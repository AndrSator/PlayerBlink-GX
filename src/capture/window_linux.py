""" Linux window capture via xdg-desktop-portal + PipeWire + GStreamer.

The Wayland security model prevents Xlib-style window enumeration. Instead
we use the ScreenCast portal (the same D-Bus API that OBS uses) which lets
the compositor show its own native picker dialog. The user selects a window
or monitor, the portal returns a PipeWire node ID, and GStreamer reads
frames from that node.

System deps (Debian 13+):
    sudo apt install pkg-config libdbus-1-dev \\
        libgirepository-2.0-dev libcairo2-dev \\
        gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 \\
        gstreamer1.0-plugins-base gstreamer1.0-plugins-good \\
        gstreamer1.0-pipewire
    pip install dbus-python PyGObject
"""
import os

import numpy as np

from src.log import logger

from .window import Window, WindowCapturer, WindowEnumerator

# Lazy-loaded at first use (see _ensure_deps)
_deps_loaded = False


def _ensure_deps():
    """ Import Linux-only deps on first call. Raises RuntimeError with a
    human-readable message if something is missing. """
    global _deps_loaded
    if _deps_loaded:
        return
    try:
        import dbus                                          # noqa: F401
        from dbus.mainloop.glib import DBusGMainLoop         # noqa: F401
        DBusGMainLoop(set_as_default=True)

        import gi
        gi.require_version("Gst", "1.0")
        gi.require_version("GstApp", "1.0")
        from gi.repository import Gst, GstApp                # noqa: F401
        Gst.init(None)

    except ImportError as e:
        raise RuntimeError(
            "PipeWire window capture requires system packages: "
            "python3-dbus python3-gi gir1.2-gstreamer-1.0 "
            "gir1.2-gstapp-1.0 gstreamer1.0-pipewire. "
            f"Missing: {e}"
        ) from e

    _deps_loaded = True


# ---------------------------------------------------------------------------
# Portal session (D-Bus flow: CreateSession → SelectSources → Start)
# ---------------------------------------------------------------------------

class _PortalSession:
    """ Synchronous wrapper around the async xdg-desktop-portal ScreenCast
    D-Bus API. Designed to run on a **worker thread** — it spins a short-
    lived GLib MainLoop to receive the three response signals and then
    returns the PipeWire node_id (or raises on error/cancel). """

    PORTAL_BUS = "org.freedesktop.portal.Desktop"
    PORTAL_PATH = "/org/freedesktop/portal/desktop"
    PORTAL_REQUEST = "org.freedesktop.portal.Request"
    PORTAL_SCREENCAST = "org.freedesktop.portal.ScreenCast"

    # SelectSources `types` flag — 1=monitor, 2=window, 3=both
    SOURCE_TYPE_WINDOW = 2

    def __init__(self):
        self._node_id: int | None = None
        self._error: str | None = None
        self._loop = None
        self._session_handle: str | None = None
        self._bus = None
        self._iface = None
        # Unique suffix per instance so D-Bus request paths and session
        # handles never collide across multiple PortalSession objects on
        # the same (singleton) SessionBus.
        self._uid = f"{id(self):x}"

    def run(self) -> int:
        """ Block until the user picks a window. Returns node_id.
        Raises RuntimeError on failure or cancellation. """
        import dbus
        from gi.repository import GLib

        self._loop = GLib.MainLoop()
        self._bus = dbus.SessionBus()

        portal_obj = self._bus.get_object(
            self.PORTAL_BUS, self.PORTAL_PATH)
        self._iface = dbus.Interface(portal_obj, self.PORTAL_SCREENCAST)

        logger.debug("[PortalSession] CreateSession...")
        self._create_session()
        self._loop.run()

        if self._error:
            raise RuntimeError(
                f"[PortalSession] {self._error}")
        if self._node_id is None:
            raise RuntimeError(
                "[PortalSession] No PipeWire node returned")

        logger.debug(
            f"[PortalSession] Success — PipeWire node {self._node_id}")
        return self._node_id

    @property
    def session_handle(self) -> str | None:
        return self._session_handle

    # -- internal helpers --------------------------------------------------

    def _request_path(self, token: str) -> str:
        import dbus
        sender = self._bus.get_unique_name().replace(".", "_").lstrip(":")
        return f"{self.PORTAL_PATH}/request/{sender}/{token}"

    def _subscribe(self, token: str, handler):
        import dbus
        path = self._request_path(token)
        self._bus.add_signal_receiver(
            handler,
            signal_name="Response",
            dbus_interface=self.PORTAL_REQUEST,
            bus_name=self.PORTAL_BUS,
            path=path,
        )

    # Step 1 ---------------------------------------------------------------
    def _create_session(self):
        import dbus
        token = f"cs_{self._uid}"
        self._subscribe(token, self._on_create_session)
        self._iface.CreateSession(dbus.Dictionary({
            "handle_token": token,
            "session_handle_token": f"sess_{self._uid}",
        }, signature="sv"))

    def _on_create_session(self, code, result):
        if code != 0:
            self._error = f"CreateSession rejected (code {code})"
            self._loop.quit()
            return

        self._session_handle = str(result["session_handle"])
        logger.debug(
            f"[PortalSession] Session: {self._session_handle}")
        self._select_sources()

    # Step 2 ---------------------------------------------------------------
    def _select_sources(self):
        import dbus
        token = f"ss_{self._uid}"
        self._subscribe(token, self._on_select_sources)
        self._iface.SelectSources(
            self._session_handle,
            dbus.Dictionary({
                "handle_token": token,
                "types": dbus.UInt32(self.SOURCE_TYPE_WINDOW),
                "multiple": False,
            }, signature="sv"),
        )

    def _on_select_sources(self, code, result):
        if code != 0:
            self._error = (
                "Window selection cancelled" if code == 1
                else f"SelectSources rejected (code {code})")
            self._loop.quit()
            return

        logger.debug("[PortalSession] Sources selected, starting stream...")
        self._start()

    # Step 3 ---------------------------------------------------------------
    def _start(self):
        import dbus
        token = f"st_{self._uid}"
        self._subscribe(token, self._on_start)
        self._iface.Start(
            self._session_handle,
            "",  # parent_window (empty = no parent)
            dbus.Dictionary({"handle_token": token}, signature="sv"),
        )

    def _on_start(self, code, result):
        if code != 0:
            self._error = (
                "Capture start cancelled" if code == 1
                else f"Start rejected (code {code})")
            self._loop.quit()
            return

        streams = result.get("streams", [])
        if not streams:
            self._error = "Portal returned no streams"
            self._loop.quit()
            return

        self._node_id = int(streams[0][0])
        props = dict(streams[0][1]) if len(streams[0]) > 1 else {}
        logger.debug(
            f"[PortalSession] Stream node={self._node_id} props={props}")
        self._loop.quit()


# ---------------------------------------------------------------------------
# GStreamer-based PipeWire frame reader
# ---------------------------------------------------------------------------

class PipeWireCapturer(WindowCapturer):
    """ Reads BGR frames from a PipeWire node via GStreamer.

    Pipeline: ``pipewiresrc → videoconvert → video/x-raw,format=BGR →
    appsink``. The appsink runs in pull mode with ``max-buffers=1
    drop=true`` so we always get the latest frame with minimal latency.
    """

    # If try_pull_sample returns None this many consecutive times (1 s
    # each), we consider the stream dead (e.g. window resized and the
    # compositor dropped the PipeWire stream). read() then raises so the
    # capture loop transitions to ERROR instead of freezing forever on
    # the last frame.
    MAX_CONSECUTIVE_TIMEOUTS = 3

    # How many times to attempt a pipeline restart before giving up.
    MAX_RESTART_ATTEMPTS = 3

    def __init__(self, node_id: int, session_handle: str | None = None):
        from gi.repository import Gst

        self._node_id = node_id
        self._session_handle = session_handle
        self._released = False
        self._first_frame_logged = False
        self._consecutive_timeouts = 0
        self._restart_count = 0

        self._build_and_start_pipeline()

    def _build_and_start_pipeline(self):
        """ Create (or recreate) the GStreamer pipeline and start it. """
        from gi.repository import Gst

        pipeline_str = (
            f"pipewiresrc path={self._node_id} do-timestamp=true ! "
            f"videoconvert ! "
            f"video/x-raw,format=BGR ! "
            f"appsink name=sink emit-signals=false "
            f"drop=true max-buffers=1"
        )

        logger.debug(
            f"[PipeWireCapturer] Pipeline: {pipeline_str}")

        self._pipeline = Gst.parse_launch(pipeline_str)
        self._appsink = self._pipeline.get_by_name("sink")

        ret = self._pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            raise RuntimeError(
                f"GStreamer pipeline failed to start for node "
                f"{self._node_id}")

        logger.debug(
            f"[PipeWireCapturer] Pipeline started for node {self._node_id}")

    def _restart_pipeline(self) -> bool:
        """ Stop the current pipeline and build a new one on the same
        PipeWire node. Returns True on success, False if exhausted. """
        from gi.repository import Gst

        self._restart_count += 1
        if self._restart_count > self.MAX_RESTART_ATTEMPTS:
            logger.warning(
                f"[PipeWireCapturer] Exhausted {self.MAX_RESTART_ATTEMPTS} "
                f"restart attempts — giving up")
            return False

        logger.info(
            f"[PipeWireCapturer] Restarting pipeline on node "
            f"{self._node_id} (attempt {self._restart_count}/"
            f"{self.MAX_RESTART_ATTEMPTS})")

        # Tear down old pipeline
        self._pipeline.set_state(Gst.State.NULL)

        # Small delay to let PipeWire settle after renegotiation
        import time
        time.sleep(0.5)

        try:
            self._build_and_start_pipeline()
        except RuntimeError as e:
            logger.warning(f"[PipeWireCapturer] Restart failed: {e}")
            return False

        self._consecutive_timeouts = 0
        self._first_frame_logged = False
        return True

    def read(self):
        from gi.repository import Gst

        if self._released:
            return False, None

        # Block up to 1 second for the next frame. Returns None on
        # timeout or EOS (e.g. when the captured window is closed).
        #
        # Some PyGObject/GStreamer versions expose try_pull_sample as a
        # method, others require the GObject signal emit path. We try
        # both to stay compatible across distros.
        try:
            sample = self._appsink.try_pull_sample(Gst.SECOND)
        except AttributeError:
            sample = self._appsink.emit("try-pull-sample", Gst.SECOND)

        if sample is None:
            self._consecutive_timeouts += 1
            if self._consecutive_timeouts >= self.MAX_CONSECUTIVE_TIMEOUTS:
                logger.warning(
                    f"[PipeWireCapturer] No frames for "
                    f"{self._consecutive_timeouts}s — stream likely dead "
                    f"(window resized or closed?)")
                # Try restarting the pipeline before giving up
                if self._restart_pipeline():
                    return False, None
                raise RuntimeError(
                    "PipeWire stream stopped delivering frames")
            return False, None

        self._consecutive_timeouts = 0
        # Reset restart counter on successful frame — the stream is
        # healthy again, so future stalls get fresh retry budget.
        self._restart_count = 0

        buf = sample.get_buffer()
        caps = sample.get_caps()
        struct = caps.get_structure(0)

        width = struct.get_value("width")
        height = struct.get_value("height")

        success, map_info = buf.map(Gst.MapFlags.READ)
        if not success:
            return False, None

        try:
            data = np.frombuffer(map_info.data, dtype=np.uint8)
            packed_size = width * height * 3

            if data.size == packed_size:
                # Rows are tightly packed — fast path
                frame = data.reshape((height, width, 3))
            else:
                # Row padding: PipeWire aligns rows to 4 bytes (or more).
                # Use numpy strides to skip the padding bytes per row
                # without copying the entire buffer.
                stride = data.size // height
                if not self._first_frame_logged:
                    logger.debug(
                        f"[PipeWireCapturer] Row padding: "
                        f"stride={stride} packed={width * 3}")
                frame = np.ndarray(
                    shape=(height, width, 3),
                    dtype=np.uint8,
                    buffer=data.data,
                    strides=(stride, 3, 1),
                )

            frame = np.ascontiguousarray(frame)
        finally:
            buf.unmap(map_info)

        if not self._first_frame_logged:
            self._first_frame_logged = True
            logger.debug(
                f"[PipeWireCapturer] First frame: "
                f"{width}x{height} BGR")

        return True, frame

    def release(self):
        if self._released:
            return

        self._released = True

        from gi.repository import Gst
        self._pipeline.set_state(Gst.State.NULL)
        logger.debug("[PipeWireCapturer] Pipeline released")

        # Close the portal session so the compositor drops the recording
        # indicator from the system tray. Without this, each capture
        # session leaves a stale "screen is being shared" icon.
        if self._session_handle:
            try:
                import dbus
                bus = dbus.SessionBus()
                session_obj = bus.get_object(
                    "org.freedesktop.portal.Desktop",
                    self._session_handle)
                session_obj.Close(
                    dbus_interface="org.freedesktop.portal.Session")
                logger.debug(
                    f"[PipeWireCapturer] Portal session closed: "
                    f"{self._session_handle}")
            except Exception as e:
                logger.warning(
                    f"[PipeWireCapturer] Failed to close portal session: "
                    f"{e}")
            self._session_handle = None


# ---------------------------------------------------------------------------
# Public enumerator interface
# ---------------------------------------------------------------------------

class LinuxWindowEnumerator(WindowEnumerator):
    """ Window capture on Linux via xdg-desktop-portal + PipeWire.

    Instead of enumerating windows itself (impossible on Wayland), the
    enumerator returns a single placeholder entry. When the user selects
    it and starts capture, ``open_capture`` triggers the compositor's
    native window picker via the ScreenCast portal. Once the user picks
    a window, a GStreamer/PipeWire pipeline delivers frames.
    """

    _PLACEHOLDER_UID = "__portal__"
    _PLACEHOLDER_TITLE = "Select window via portal..."

    def _enumerate(self) -> list[Window]:
        # pid=-1 so the placeholder is NOT filtered by the self-PID
        # exclusion in list_windows(). The placeholder is a synthetic
        # entry that triggers the portal dialog, not a real window.
        placeholder = Window(
            uid=self._PLACEHOLDER_UID,
            title=self._PLACEHOLDER_TITLE,
            pid=-1,
            native=None,
        )
        logger.debug(
            f"[LinuxWindowEnum] _enumerate: returning placeholder "
            f"uid={placeholder.uid!r} title={placeholder.title!r}")
        return [placeholder]

    def is_minimized(self, window: Window) -> bool:
        # PipeWire streams don't expose minimized state. The stream
        # keeps delivering frames (or freezes the last one) regardless.
        return False

    def open_capture(self, window: Window) -> WindowCapturer:
        """ Trigger the portal picker and return a PipeWire capturer.

        This call **blocks** until the user selects a window in the
        compositor dialog. It's meant to be called from the capture
        worker thread, not the UI thread.
        """
        logger.debug("[LinuxWindowEnum] open_capture: loading deps...")
        _ensure_deps()

        logger.debug("[LinuxWindowEnum] open_capture: starting portal session")
        session = _PortalSession()
        node_id = session.run()

        logger.debug(
            f"[LinuxWindowEnum] open_capture: creating PipeWire capturer "
            f"for node {node_id}")
        return PipeWireCapturer(
            node_id, session_handle=session.session_handle)
