import taichi as ti
from taichi.math import vec2


ti.init(arch=ti.gpu, default_ip=ti.i32, default_fp=ti.f32, debug=False)

image_resolution = (512, 512)

SAMPLES_PER_FRAME = 1
SAMPLES_PER_PIXEL = 1  # number of samples in one draw call
QUALITY_PER_SAMPLE = 0.8  # for russian roulette

BLACK_BACKGROUND = True
ADAPTIVE_SAMPLING = True

VISIBILITY = vec2(1e-4, 1e4)
NOISE_THRESHOLD = 1e-4  # for self-adaptive sampling

SCREEN_PIXEL_SIZE = 1.0 / vec2(image_resolution)
PIXEL_RADIUS = 0.5 * SCREEN_PIXEL_SIZE.min()

MIN_DIS = 2.5 * PIXEL_RADIUS
MAX_DIS = 1e3

MAX_RAYMARCH = 512
MAX_RAYTRACE = 3

ENV_IOR = 1.000277
