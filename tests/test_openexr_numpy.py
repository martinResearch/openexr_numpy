"""Module to read and write EXR image files into and from numpy arrays."""

import os

import imageio.v3 as imageio
import numpy as np

from openexr_numpy import imread, imwrite

# Enabling openexr support in opencv by settign the
# OPENCV_IO_ENABLE_OPENEXR environment variable
# This need to be done before the first import of opencv import on windows
# which violate pep8 import rules https://peps.python.org/pep-0008/#imports
# and can be tricky to ensure if the opencv  is imported in other modules.
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2  # noqa: E402


def test_exr() -> None:

    # test round trip with float32 1 channel
    rgb_image = np.random.rand(12, 30).astype(np.float32)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test round trip with float16 1 channel
    rgb_image = np.random.rand(12, 30).astype(np.float16)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test round trip with uint32 1 channel
    rgb_image = np.random.rand(12, 30).astype(np.uint32)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test round trip with float32 3 channels
    rgb_image = np.random.rand(12, 30, 3).astype(np.float32)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test round trip with float16 3 channels
    rgb_image = np.random.rand(12, 30, 3).astype(np.float16)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test round trip with uint32 3 channels
    rgb_image = np.random.rand(12, 30, 3).astype(np.uint32)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test round trip with float32 4 channels
    rgb_image = np.random.rand(12, 30, 4).astype(np.float32)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test round trip with float16 4 channels
    rgb_image = np.random.rand(12, 30, 4).astype(np.float16)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test round trip with uint32 4 channels
    rgb_image = np.random.rand(12, 30, 4).astype(np.uint32)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)

    # test reading a subset of channels
    rgb_image = np.random.rand(12, 30, 4).astype(np.uint32)
    file_path = "test.exr"
    imwrite(file_path, rgb_image)
    channel_r = imread(file_path, "R")
    assert np.allclose(rgb_image[:, :, 0], channel_r)

    # test channel names convention consistency with opencv when using 1 channel
    grey_image = np.random.rand(12, 30).astype(np.float32)
    file_path = "test.exr"
    cv2.imwrite(file_path, grey_image)
    grey_image_a = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    grey_image_b = imread(file_path)
    assert np.allclose(grey_image, grey_image_a)
    assert np.allclose(grey_image_b, grey_image_a)

    # test channel names convention w.r.t opencv when using 3 channels
    # opencv uses BGR while we use RGB when the image has 3 channels
    bgr_image = np.random.rand(12, 30, 3).astype(np.float32)
    file_path = "test.exr"
    cv2.imwrite(file_path, bgr_image)
    bgr_image_a = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    bgr_image_b = imread(file_path)[:, :, ::-1]
    assert np.allclose(rgb_image, rgb_image_b)
    assert np.allclose(bgr_image_a, bgr_image_b)
    rgb_image_b = imread(file_path, channel_names="BGR")[:, :, ::-1]
    assert np.allclose(bgr_image, bgr_image_b)

    # test channel names convention w.r.t opencv when using 4 channels
    # opencv uses BGRA while we use RGBA when the image has 3 channels
    bgra_image = np.random.rand(12, 30, 4).astype(np.float32)
    file_path = "test.exr"
    cv2.imwrite(file_path, bgra_image)
    bgra_image_a = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    bgra_image_b = imread(file_path, "BGRA")
    assert np.allclose(bgra_image_a, bgra_image)
    assert np.allclose(bgra_image_b, bgra_image)

    # test channel names convention consistency with imageio when using 3 channels
    # imageio save the data as float16 and convert to float32 after loading
    # when using the freeimage plugin (which requires to run a download
    # step and modifies the system path)
    # imageio opencv's plugin loads the image as unit8
    rgba_image = np.random.rand(12, 30, 3).astype(np.float32)
    file_path ="test.exr"
    imageio.imwrite(file_path, rgba_image)
    rgba_image_a = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)[:, :, ::-1]
    rgba_image_b = imread(file_path)
    assert np.allclose(rgba_image.astype(np.float16), rgba_image_b.astype(np.float16))
    assert np.allclose(rgba_image_a.astype(np.float16), rgba_image_b.astype(np.float16))

    # test channel names convention consistency with imageio when using 4 channels
    # imageio seems to converts to float16 silently
    rgb_image = np.random.rand(12, 30, 4).astype(np.float32)
    file_path = "test.exr"
    imageio.imwrite(file_path, rgb_image)
    rgb_image_a = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)[:, :, [2, 1, 0, 3]]
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image.astype(np.float16), rgb_image_b.astype(np.float16))
    assert np.allclose(rgb_image_a.astype(np.float16), rgb_image_b.astype(np.float16))

    # test consistency with imageio when using 1 channel
    # imageio convert the image to float16 silently
    grey_image = np.random.rand(12, 30).astype(np.float32)
    file_path = "test.exr"
    imageio.imwrite(file_path, grey_image)
    grey_image_a = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    grey_image_b = imread(file_path)
    assert np.allclose(grey_image.astype(np.float16), grey_image_b.astype(np.float16))
    assert np.allclose(grey_image_a, grey_image_b)


if __name__ == "__main__":
    test_exr()
