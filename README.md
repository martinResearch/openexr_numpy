# openexr_numpy

Making reading and writing OpenEXR images in python easy using numpy arrays.

## Motivation

Writing and reading exr image with existing package [imageio](https://imageio.readthedocs.io/en/stable/), [opencv-python](https://pypi.org/project/opencv-python/) or [OpenEXR](https://pypi.org/project/OpenEXR/) has currently inconvenient limitations:

* [opencv-python](https://pypi.org/project/opencv-python/) allows to save and read exr images but it requires to 
set up a environment variable OPENCV_IO_ENABLE_OPENEXR before the first import of opencv on windows, which violate pep8 [import rules](https://peps.python.org/pep-0008/#imports) and can be tricky to ensure if the opencv is imported in other modules. See issue [here](https://github.com/opencv/opencv/issues/24470).

* [imageio](https://imageio.readthedocs.io/en/stable/) uses either [freeimage](https://freeimage.sourceforge.io/) or the opencv under the hood to load and read exr images. Freeimage does not have a permissive license and thus is not installed by default with imageio and cannot be installed with pip (see issue [here](https://github.com/imageio/imageio/issues/809)). Installing it requires a [manual step](https://imageio.readthedocs.io/en/stable/_autosummary/imageio.plugins.freeimage.html#module-imageio.plugins.freeimage) that departs from the traditional Python environment setup process using pip only and modifies the system by adding the freeimage dll in the system path, making it visible to all python environments and thus potentially modifying the behaviour of other python environment that use imageio on the machine. Using opencv under the hood has also limitations as it requires to setup an environment variable (see above). 

* [OpenEXR](https://pypi.org/project/OpenEXR/). This is the official python binding for the OpenEXR file format. The documentation for the python API is very limited and the API is quite verbose. 

Our package is a wrapper around OpenEXR binding that: 
* can be installed with pip
* does not require to setup any environment variable before any import 
* provides a simple API using numpy arrays that is similar to the APIs used in opencv and imageio. 

## Example usage 

### Using imread and imwrite
```
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
bgr_image = rgb_image[:,:,::-1]
imwrite(file_path, bgr_image, channel_names="BGR")

# read the image with a chosen channel order
brg_image_loaded = imread(file_path, channel_names="BGR")

# check consistency
assert np.allclose(red_channel, rgb_image[:, :, 0])
assert np.allclose(rgb_image, rgb_image_loaded)
assert np.allclose(bgr_image, brg_image_loaded)
```


More examples can be found in the tests file [test_openexr_numpy](tests/test_openexr_numpy.py).

The default convention we use for the channel names in the exr file is follows the convention used by imageio and is defined in the global variable `default_channel_names` defined as
```
default_channel_names: Dict[int, tuple[str, ...]] = {
    1: ("Y",),
    3: ("R", "G", "B"),
    4: ("R", "G", "B", "A"),
}
```
This convention differs from opencv that uses BGR and BGRA respectively for 3 and 4 channels.
The channels ordering default convention can modified by the user using the function `set_default_channel_names`, but we recommend providing explicitly the names of the channels when calling `imread` and `imwrite` instead using the `channel_names` argument.

### Using dictionaries

One can use the function `read` and `write` to get more flexible lower level access to OpenEXR with different data type for each channel: 
```
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
```
Each data channel value should be an numpy arrays of dimension 2 and all arrays should have the same width and height.


### Using numpy structured arrays

The `read` and `write` functions also support [numpy structured arrays](https://numpy.org/doc/stable/user/basics.rec.html). The 
`write` function can take a structure array as input and one simply needs to provide the argument  `structured=True` when reading the data to get back a structured array instead of a dictionary.

Note that the names in the dtype need to be alphabetically sorted in order to get back the same dtype when loading the data.

Example:
```
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
 ```



