"""Module to read and write EXR image files into and from numpy arrays."""

import os

import imageio.v3 as imageio
import numpy as np

from openexr_numpy import imread, imwrite, read, write

# Enabling openexr support in opencv by settign the
# OPENCV_IO_ENABLE_OPENEXR environment variable
# This need to be done before the first import of opencv import on windows
# which violate pep8 import rules https://peps.python.org/pep-0008/#imports
# and can be tricky to ensure if the opencv  is imported in other modules.
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2  # noqa: E402


def test_readme_example() -> None:

    # generate a 3 channel image
    rgb_image = np.random.rand(12, 30, 3).astype(np.float32)
    file_path = "test.exr"

    # write the image
    imwrite(file_path, rgb_image)

    # read the image
    rgb_image_loaded = imread(file_path)

    # read a single channel
    red_channel = imread(file_path, "R")

    # write the image with explicit channel names
    bgr_image = rgb_image[:, :, ::-1]
    imwrite(file_path, bgr_image, channel_names="BGR")

    # read the image with a chosen channel order
    brg_image_loaded = imread(file_path, channel_names="BGR")

    # check consistency
    assert np.allclose(red_channel, rgb_image[:, :, 0])
    assert np.allclose(rgb_image, rgb_image_loaded)
    assert np.allclose(bgr_image, brg_image_loaded)


def test_imread_imwrite_round_trips() -> None:

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


def test_using_dicts() -> None:
    # Create a two-channel image with different types and custom names
    data = {
        "red": np.random.rand(12, 30).astype(np.float32),
        "green": np.random.rand(12, 30).astype(np.uint32),
    }
    file_path = "test.exr"

    # Write the data
    write(file_path, data)

    # Read the data
    data_b = read(file_path)

    # Check the process is lossless
    assert np.allclose(data["red"], data_b["red"])
    assert np.allclose(data["green"], data_b["green"])


def test_against_opencv() -> None:

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
    assert np.allclose(bgr_image_a, bgr_image_b)
    bgr_image_b = imread(file_path, channel_names="BGR")
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


def test_against_imageio() -> None:
    # test channel names convention consistency with imageio when using 3 channels
    # imageio save the data as float16 and convert to float32 after loading
    # when using the freeimage plugin (which requires to run a download
    # step and modifies the system path)
    # imageio opencv's plugin loads the image as unit8
    rgba_image = np.random.rand(12, 30, 3).astype(np.float32)
    file_path = "test.exr"
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


def test_using_structured_arrays() -> None:
    # Define the structured array type
    dtype = np.dtype([("green", np.float32), ("red", np.uint32)])

    # Initialize the structured array with zeros
    data = np.zeros((12, 30), dtype=dtype)
    data["red"] = np.random.rand(12, 30).astype(np.float32)
    data["green"] = np.random.rand(12, 30).astype(np.uint32)

    # Write the data
    file_path = "test.exr"
    write(file_path, data)

    # Read the data
    data_loaded = read(file_path, structured=True)

    # Check the process is lossless
    assert data_loaded.dtype == dtype
    assert np.allclose(data["red"], data_loaded["red"])
    assert np.allclose(data["green"], data_loaded["green"])


if __name__ == "__main__":
    test_using_dicts()
    test_using_structured_arrays()
    test_readme_example()
    test_against_imageio()
    test_against_opencv()
