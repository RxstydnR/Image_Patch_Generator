# Patch Image Generator using OpenCV

## Running

```bash
python image_patch_generator.py \\
        --dataset [Path to folder storing images] \\
        --save [Path to saving folder] \\
        --patch_size [Size of patch image size] 
```

The generated patch images are limited to square images. By changing the code, you can create flexible patch images.

### Example

```bash
python image_patch_generator.py --dataset img --save patch --patch_size 32
```



## How to use

<center><img src="demo/demo.png" width=700></center>

- **Cut out**

  click

- **Move to the next image**

  press "k" key

- **Exit**

  press "q" key

The image on the left is a screen for specifying the patch image area. 
When you click on the image, the patch image centered on the clicked point is cut out. 
The cropped patch image is displayed in the upper left corner and is saved in the saving folder. 
To move to the next image, press the "k" button. 
As long as you do not move to the next image, you can continue to cut the patch image from the same image. 
To exit the program, press "q".
