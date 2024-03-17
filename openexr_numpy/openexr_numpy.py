"""Module to read and write EXR image files into and from numpy arrays."""

import numpy as np
import os
import OpenEXR
import Imath
import imageio.v3 as imageio
from typing import Optional, Iterable

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2


FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
UINT = Imath.PixelType(Imath.PixelType.UINT)
HALF = Imath.PixelType(Imath.PixelType.HALF)

# conventions for channel names according to the number of channels
channels_names_convention = {1: ("Y"), 3: ("R", "G", "B"), 4: ("R", "G", "B", "A")}


def imwrite(file_path, image, channel_names: Optional[Iterable[str]] = None):

    if image.dtype not in [np.dtype("float16"), np.dtype("float32"), np.dtype("uint32")]:
        raise ValueError("The image must be of type float16, float32 or uint32.")

    # Create an OpenEXR header
    width, height = image.shape[1], image.shape[0]
    header = OpenEXR.Header(width, height)

    # Determine number of channels
    if image.ndim not in [2, 3]:
        raise ValueError(f"Unsupported number of dimensions {image.ndim}, must be 2 or 3.")
    if image.ndim == 2:
        image = image[..., np.newaxis]
    num_channels = image.shape[2]
    if channel_names is None:
        if num_channels not in channels_names_convention:
            raise ValueError(
                f"Unsupported number of channels {num_channels}, must be in {channels_names_convention.keys()}."
            )
        channels_names = channels_names_convention[num_channels]
    if not num_channels == len(channels_names):
        raise ValueError(f"Error in the channels_names {channels_names} should be of length {num_channels}.")

    exr_type = {np.dtype("float16"): HALF, np.dtype("float32"): FLOAT, np.dtype("uint32"): UINT}[image.dtype]

    # Write each channel
    header["channels"] = {channel: Imath.Channel(exr_type) for channel in channels_names}
    channels = {channel: image[..., i].tobytes() for i, channel in enumerate(channels_names)}

    # Create the EXR file
    exr_file = OpenEXR.OutputFile(file_path, header)

    # Write the image data to the file
    exr_file.writePixels(channels)

    # Close the file
    exr_file.close()


def imread(file_path: str, channel_names: Optional[Iterable[str]] = None) -> np.ndarray:
    # Open the EXR file
    exr_file = OpenEXR.InputFile(file_path)

    # Get the image header (contains information about the image)
    header = exr_file.header()

    # Get the image size
    size = (
        header["dataWindow"].max.x - header["dataWindow"].min.x + 1,
        header["dataWindow"].max.y - header["dataWindow"].min.y + 1,
    )

    # Get the channel names
    exr_channel_names = list(header["channels"].keys())

    # Read the image data
    data = {}

    for channel_name in exr_channel_names:
        # Read each channel as numpy array
        exr_type = header["channels"][channel_name]
        if exr_type == Imath.Channel(HALF):
            dtype = np.float16
        elif exr_type == Imath.Channel(FLOAT):
            dtype = np.float32
        elif exr_type == Imath.Channel(UINT):
            dtype = np.uint32
        data[channel_name] = np.frombuffer(exr_file.channel(channel_name), dtype=dtype)

    # Reshape the data into the image dimensions
    for channel_name in exr_channel_names:
        data[channel_name] = data[channel_name].reshape(size[1], size[0])

    num_channels = len(exr_channel_names)
    if num_channels not in channels_names_convention:
        raise ValueError(f"Unsupported number of channels {num_channels}, must be {channels_names_convention.keys()}.")

    if channel_names is None:
        if num_channels not in channels_names_convention:
            raise ValueError(
                f"Unsupported number of channels {num_channels}, must be in {channels_names_convention.keys()}."
            )
        channel_names = channels_names_convention[num_channels]

    missing_channels = [channel for channel in channel_names if channel not in exr_channel_names]
    if missing_channels:
        raise ValueError(
            f"Missing channels {missing_channels} in the file, got {exr_channel_names}, expected {channel_names}"
        )
    # Merge the channels according to the flags

    image = np.stack([data[channel] for channel in channel_names], axis=-1)
    if len(channel_names) == 1:
        image = image.squeeze()
    return image

