#version 330 core

uniform float u_time;
out vec4 fragColor;

// Well-known hash multipliers used by the screen-space PRNG below.
const vec2  HASH_DIR   = vec2(12.9898, 78.233);
const float HASH_SCALE = 43758.5453;

const float PIXEL_SIZE = 10.0;
const float NOISE_SCALE = 0.0005;

// CRT scanline modulation
const float SCANLINE_PERIOD = 0.05;
const float SCAN_INTENSITY = 1.0;
const float SCAN_BASE_BRIGHTNESS = 0.7;

const float PI = 3.14159;

float hash(vec2 p) {
    return fract(sin(dot(p, HASH_DIR)) * HASH_SCALE);
}

void main() {
    // Quantize fragment coords to the fat-pixel grid before hashing,
    // so every PIXEL_SIZE × PIXEL_SIZE block gets the same noise value.
    vec2 cell = floor(gl_FragCoord.xy / PIXEL_SIZE);

    // Time-shifted hash so each fat pixel flickers independently
    float n = hash(cell + vec2(u_time * NOISE_SCALE));

    // Soft horizontal scanlines spread over SCANLINE_PERIOD screen pixels
    float scan = SCAN_BASE_BRIGHTNESS
               + SCAN_INTENSITY * sin(gl_FragCoord.y * (2.0 * PI / SCANLINE_PERIOD));

    vec3 col = vec3(n) * scan;
    fragColor = vec4(col, 1.0);
}
