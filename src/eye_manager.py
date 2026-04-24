import os

import cv2
from PIL import Image

from PySide6.QtCore import QObject, Signal

from src.log import logger

__version__ = "1.0.0"


class EyeManager(QObject):
    """ Manage eyes and other resources for image recognition """

    # Signals
    selected_changed = Signal(object)

    def __init__(self, resources_dir=None, parent=None):
        super().__init__(parent)
        self._resources_dir = resources_dir
        self._selected_resource = None

    @property
    def resources_dir(self):
        return self._resources_dir

    @resources_dir.setter
    def resources_dir(self, path):
        if not os.path.isdir(path) or not os.access(path, os.W_OK):
            raise ValueError(f"Invalid directory path: {path}")

        self._resources_dir = path

    @property
    def selected_resource(self):
        return self._selected_resource

    @selected_resource.setter
    def selected_resource(self, resource):
        if resource is self._selected_resource:
            return

        self._selected_resource = resource
        self.selected_changed.emit(resource)

    def create_resource(self, file_name=None):
        if not file_name:
            file_name = "eye.png"

        full_path = self._resources_dir / file_name
        logger.debug(f"Creating new resource at {full_path}")

        try:
            img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
            img.save(full_path)

            logger.debug(f"{file_name} created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating new resource: {e}")
            return False

    def delete_selected(self):
        self._delete_resource_file()
        self._selected_resource = None
        self.selected_changed.emit(None)

    def _delete_resource_file(self):
        try:
            if (self._selected_resource and
                    self._selected_resource.path.exists()):
                os.remove(self._selected_resource.path)
        except Exception as e:
            logger.error(f"Error deleting {self._selected_resource}: {e}")

    def save_selected_from_array(self, image_array) -> bool:
        """ Overwrite the selected resource file with the given image array """
        resource = self._selected_resource
        if resource is None:
            return False

        cv2.imwrite(str(resource.path), image_array)
        logger.info(f"[EyeManager] Overwritten eye crop: {resource.path}")
        return True

    def load_selected_pattern(self):
        """ Return the raw image bytes of the selected resource, or None """
        if self._selected_resource is None:
            return None

        path = self._selected_resource.path

        if not path.exists():
            return None

        return path.read_bytes()
