# openexr_numpy

Making reading and writing OpenEXR images in python easy using numpy arrays.

## Motivation

Writing and reading exr image with existing package [imageio](https://imageio.readthedocs.io/en/stable/), [opencv-python](https://pypi.org/project/opencv-python/) or [OpenEXR](https://pypi.org/project/OpenEXR/) has currently unconvenient limitations:

* [opencv-python](https://pypi.org/project/opencv-python/) allows to save and read exr images but it requires to 
set up a environment variable OPENCV_IO_ENABLE_OPENEXR before the first import of opencv on windows, which violate pep8 [import rules](https://peps.python.org/pep-0008/#imports) and can be tricky to ensure if the opencv is imported in other modules. See issue [here](https://github.com/opencv/opencv/issues/24470).

* [imageio](https://imageio.readthedocs.io/en/stable/) uses either [freeimage](https://freeimage.sourceforge.io/) or the opencv under the hood to load and read exr images. Freeimage does not have a permissive license and thus is not installed by default with imageio and cannot be installed with pip (see issue [here](https://github.com/imageio/imageio/issues/809)). Installing it requires a [manual step](https://imageio.readthedocs.io/en/stable/_autosummary/imageio.plugins.freeimage.html#module-imageio.plugins.freeimage) that departs from the classical python environment setup process and modifies the system by adding the freeimage dll in the system path, making it visible to all python environments and thus potentially modifying the behaviour of other python environment that use imageio on the machine. Using opencv under the hood has also limitations as it requires to setup an environment variable (see above). 

* [OpenEXR](https://pypi.org/project/OpenEXR/). This is the official python binding for the OpenEXR file format. The documentation for the python API is very limited and the API is quite verbose. 

Our package is a wrapper around OpenEXR binding that: 
* can be installed with pip
* does not require to setup any environment variable before any import 
* provides a simple API using numpy arrays that is similar to the APIs used in opencv and imageio. 

## Example usage 

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

The default convention we use for the channels names in the exr file is follows the convention used by imageio and is defined in the global variable `default_channel_names` defined as
```
default_channel_names = {1: ("Y"), 3: ("R", "G", "B"), 4: ("R", "G", "B", "A")}
```
This convention differs from opencv that uses BGR and BGRA respectively for 3 and 4 channels.
The channels ordering default convention can modified by the user using the function `set_default_channel_names`, but we recommend providing explicitly the names of the channels when calling `imread` and `imwrite` instead using the `channel_names` argument.

 



