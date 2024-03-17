# openexr_numpy

Simple numpy interface to the OpenEXR image file format.

## Example usage 

```
    # generate a 3 channel image
    rgb_image = np.random.rand(12, 30, 3).astype(np.float32)
    file_path = "test.exr"
    
    # write the image
    imwrite(file_path, rgb_image)
    
    # read the image
    rgb_image_b = imread(file_path)

    # read a single channel
    red_channel = imread(file_path, "R")

    # write the image with explicit channel names
    bgr_image=rgb_image[:,:,::-1]
    imwrite(file_path, bgr_image, channel_names="BGR")

    # read the image with a chosen channel order
    rgb_image_c = imread(file_path, channel_names="BGR")
```

The default convention we use for the channels names in the exr file is defined
in the global variable `channels_names_convention` defined as
```
channels_names_convention = {1: ("Y"), 3: ("R", "G", "B"), 4: ("R", "G", "B", "A")}
```
This can be modified by the user, but we recommend providing explictly the names of the channels instead using the `channel_names` argument

## Alternative

* [imageio](https://imageio.readthedocs.io/en/stable/) uses the freeimage plugin to load and read exr image, but this plugin does not have a permissive license is not installed by default with imageio and cannot be installed with pip (see issue [here](https://github.com/imageio/imageio/issues/809))

* [opencv-python](https://pypi.org/project/opencv-python/) allows to save and read exr images but it requires to 
set up a environment variable before the import on windows. See issue [here](https://github.com/opencv/opencv/issues/24470).

* [OpenEXR](https://pypi.org/project/OpenEXR/). This is the official python binding. the documentation for the python API is very limited and the API is quite verbose. Our package is a wrapper around OpenEXR that provides a simpler API using numpy arrays that is similar to opencv snd imagei.o  



