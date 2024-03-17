"""Module to read and write EXR image files into and from numpy arrays."""

from typing import Dict, Iterable, Literal, Optional, Union, overload

import Imath
import numpy as np
import OpenEXR

FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
UINT = Imath.PixelType(Imath.PixelType.UINT)
HALF = Imath.PixelType(Imath.PixelType.HALF)

# conventions for channel names according to the number of channels
default_channel_names: Dict[int, tuple[str, ...]] = {
    1: ("Y",),
    3: ("R", "G", "B"),
    4: ("R", "G", "B", "A"),
}


def set_default_channel_names(num_channels: int, channel_names: Iterable[str]) -> None:
    """Set the default channel names for a given number of channels.

    Ags:
        num_channels: int, number of channels
        channel_names: Iterable[str], channel names

    """
    global default_channel_names
    if not num_channels == len(list(channel_names)):
        raise ValueError(
            f"Error in the channels_names {channel_names} "
            f"should be of length {num_channels}."
        )
    default_channel_names[num_channels] = tuple(channel_names)


def get_default_channel_names(num_channels: int) -> tuple[str, ...]:
    """Get the default channel names for a given number of channels.

    Args:
        num_channels: int, number of channels

    Returns:
        tuple[str, ...], default channel names

    """
    if num_channels not in default_channel_names:
        raise ValueError(
            f"Undefined default channel names for number of "
            f"channels {num_channels}. "
            "Default names are currently only defined for the following "
            f"number of channels: {list(default_channel_names.keys())}. "
            "You can add new default names using set_default_channel_names."
        )
    return default_channel_names[num_channels]


def read_dict(file_path: str) -> Dict[str, np.ndarray]:
    """Read the data from an EXR file.

    Args:
        file_path: str, path to the file

    Returns:
        Dict[str:np.ndarray], data

    """
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
            dtype_str = "float16"
        elif exr_type == Imath.Channel(FLOAT):
            dtype_str = "float32"
        elif exr_type == Imath.Channel(UINT):
            dtype_str = "uint32"
        data[channel_name] = np.frombuffer(
            exr_file.channel(channel_name), dtype=np.dtype(dtype_str)
        )

    # Reshape the data into the image dimensions
    for channel_name in exr_channel_names:
        data[channel_name] = data[channel_name].reshape(size[1], size[0])
    return data


def _get_shape_from_dict(channels: Dict[str, np.ndarray]) -> tuple[int, int]:
    if len(channels) == 0:
        raise ValueError("No data to write.")
    image_shape: Optional[tuple[int, int]] = None
    for name, image in channels.items():
        if not image.ndim == 2:
            raise ValueError(
                f"The data must be of shape (height, width). "
                f"the channel {name} has {image.ndim} dimensions."
            )
        if image_shape is None:
            assert len(image.shape) == 2
            height, width = image.shape
            image_shape = height, width
        if not image.shape == image_shape:
            raise ValueError("All images must have the same shape.")
    assert image_shape is not None, "image_shape should not be None at this point"
    return image_shape


def write_dict(file_path: str, channels: Dict[str, np.ndarray]) -> None:

    image_shape = _get_shape_from_dict(channels)

    exr_types = {}
    for name, image in channels.items():

        if image.dtype not in [
            np.dtype("float16"),
            np.dtype("float32"),
            np.dtype("uint32"),
        ]:
            raise ValueError(
                f"The data {name} must be of type float16, float32 or uint32."
            )
        exr_types[name] = {
            np.dtype("float16"): HALF,
            np.dtype("float32"): FLOAT,
            np.dtype("uint32"): UINT,
        }[image.dtype]

    height, width = image_shape
    header = OpenEXR.Header(width, height)

    # Write each channel
    header["channels"] = {
        name: Imath.Channel(exr_type) for name, exr_type in exr_types.items()
    }
    channels_bytes = {
        name: numpy_array.tobytes() for name, numpy_array in channels.items()
    }

    # Create the EXR file
    exr_file = OpenEXR.OutputFile(file_path, header)

    # Write the image data to the file
    exr_file.writePixels(channels_bytes)

    # Close the file
    exr_file.close()


def dict_to_structured_array(data: Dict[str, np.ndarray]) -> np.ndarray:
    """Convert a dictionary of numpy arrays to a structured numpy array.

    Args:
        data: Dict[str, np.ndarray], data

    Returns:
        np.ndarray, structured array

    """
    # Create the structured array
    dtype = [(name, channel.dtype) for name, channel in data.items()]
    image_shape = _get_shape_from_dict(data)
    structured_array = np.empty(image_shape, dtype=dtype)

    # Fill the structured array
    for name, array in data.items():
        structured_array[name] = array
    return structured_array


def dict_from_structured_array(structured_array: np.ndarray) -> Dict[str, np.ndarray]:
    channels = {
        name: structured_array[name] for name in structured_array.dtype.fields.keys()
    }
    return channels


def read_structured_array(file_path: str) -> np.ndarray:
    """Read the data from an EXR file as a structured numpy array."""
    return dict_to_structured_array(read_dict(file_path))


def write_structured_array(file_path: str, structured_array: np.ndarray) -> None:
    """Write a structured numpy array to an EXR file."""
    names = list(structured_array.dtype.fields.keys())
    # check the names are sorted alphabetically
    if not names == sorted(names):
        raise ValueError(
            "The names of the fields in the structured array "
            "must be sorted alphabetically in order for the data"
            "to be loaded in the same order from the exr file."
        )
    write_dict(file_path, dict_from_structured_array(structured_array))


@overload
def read(file_path: str) -> Dict[str, np.ndarray]:
    ...


@overload
def read(file_path: str, structured: Literal[False]) -> Dict[str, np.ndarray]:
    ...


@overload
def read(file_path: str, structured: Literal[True]) -> np.ndarray:
    ...


def read(
    file_path: str, structured: bool = False
) -> Union[np.ndarray, Dict[str, np.ndarray]]:
    """Read the data from an EXR file as a structured numpy array."""
    if structured:
        return read_structured_array(file_path)
    else:
        return read_dict(file_path)


def write(file_path: str, data: Union[np.ndarray, Dict[str, np.ndarray]]) -> None:
    """Write a structured numpy array or dict to an EXR file."""
    if isinstance(data, np.ndarray):
        write_structured_array(file_path, data)
    else:
        write_dict(file_path, data)


def imwrite(
    file_path: str, image: np.ndarray, channel_names: Optional[Iterable[str]] = None
) -> None:
    """Write an image to an EXR file.

    Args:
        file_path: str, path to the file
        image: np.ndarray, image to write
        channel_names: Optional[Iterable[str]], channel names

    """
    if image.dtype not in [
        np.dtype("float16"),
        np.dtype("float32"),
        np.dtype("uint32"),
    ]:
        raise ValueError("The image must be of type float16, float32 or uint32.")

    # Determine number of channels
    if image.ndim not in [2, 3]:
        raise ValueError(
            f"Unsupported number of dimensions {image.ndim}, must be 2 or 3."
        )
    if image.ndim == 2:
        image = image[..., np.newaxis]
    num_channels = image.shape[2]
    if channel_names is None:
        channel_names = get_default_channel_names(num_channels)
    assert channel_names is not None
    if not num_channels == len(list(channel_names)):
        raise ValueError(
            f"Error in the channels_names {channel_names} "
            f"should be of length {num_channels}."
        )

    channels = {channel: image[..., i] for i, channel in enumerate(channel_names)}
    write_dict(file_path, channels)


def imread(file_path: str, channel_names: Optional[Iterable[str]] = None) -> np.ndarray:
    """Read an image from an EXR file.

    Args:
        file_path: str, path to the file
        channel_names: Optional[Iterable[str]], channel names

    Returns:
        np.ndarray, image

    """
    data = read_dict(file_path)

    exr_channel_names = list(data.keys())
    num_channels = len(exr_channel_names)

    if channel_names is None:
        channel_names = get_default_channel_names(num_channels)

    missing_channels = [
        channel for channel in channel_names if channel not in exr_channel_names
    ]
    if missing_channels:
        raise ValueError(
            f"Missing channels {missing_channels} in the file, "
            f"got {exr_channel_names}, expected {channel_names}"
        )

    # Merge the channels
    image = np.stack([data[channel] for channel in channel_names], axis=-1)
    if len(list(channel_names)) == 1:
        image = image.squeeze()
    return image
