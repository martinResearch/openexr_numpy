"""Module to read and write EXR image files into and from numpy arrays."""

import os

import imageio.v3 as imageio
import numpy as np

from openexr_numpy import imread, imwrite

# enable openexr support in opencv
# this need to be done before the import on windows
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
    rgb_image = np.random.rand(12, 30).astype(np.float32)
    file_path = "test.exr"
    cv2.imwrite(file_path, rgb_image)
    rgb_image_a = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image, rgb_image_b)
    assert np.allclose(rgb_image_a, rgb_image_b)

    # test channel names convention consistency with opencv when using 4 channels
    # opencv silently convert to float16 when saving to file when using 4 channels
    rgb_image = np.random.rand(12, 30, 4).astype(np.float32)
    file_path = "test.exr"
    imageio.imwrite(file_path, rgb_image)
    rgb_image_a = imageio.imread(file_path)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image.astype(np.float16), rgb_image_a)
    assert np.allclose(rgb_image_a, rgb_image_b)

    # test channel names convention consistency with opencv when using 3 channels
    # opencv uses BGR while we use RGB when the image has 3 channels
    rgb_image = np.random.rand(12, 30, 3).astype(np.float32)
    file_path = "test.exr"
    cv2.imwrite(file_path, rgb_image)
    rgb_image_a = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    rgb_image_b = imread(file_path)[:, :, ::-1]
    assert np.allclose(rgb_image, rgb_image_b)
    assert np.allclose(rgb_image_a, rgb_image_b)
    rgb_image_b = imread(file_path, channel_names="BGR")[:, :, ::-1]

    # test channel names convention consistency with imageio when using 3 channels
    # imageio converts to float16 silently
    rgb_image = np.random.rand(12, 30, 3).astype(np.float32)
    file_path = "test.exr"
    imageio.imwrite(file_path, rgb_image)
    rgb_image_a = imageio.imread(file_path)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image.astype(np.float16), rgb_image_b)
    assert np.allclose(rgb_image_a, rgb_image_b)

    # test channel names convention consistency with imageio when using 4 channels
    # imageio converts to float16 silently
    rgb_image = np.random.rand(12, 30, 4).astype(np.float32)
    file_path = "test.exr"
    imageio.imwrite(file_path, rgb_image)
    rgb_image_a = imageio.imread(file_path)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image.astype(np.float16), rgb_image_b)
    assert np.allclose(rgb_image_a, rgb_image_b)

    # test consistency with imageio when using 1 channel
    # imageio convert the image to float16 silently
    rgb_image = np.random.rand(12, 30).astype(np.float32)
    file_path = "test.exr"
    imageio.imwrite(file_path, rgb_image)
    rgb_image_a = imageio.imread(file_path)
    rgb_image_b = imread(file_path)
    assert np.allclose(rgb_image.astype(np.float16), rgb_image_b)
    assert np.allclose(rgb_image_a, rgb_image_b)


if __name__ == "__main__":
    test_exr()
