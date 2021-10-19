import warnings
warnings.simplefilter('ignore')

import cv2
import glob
import os
import argparse

def onMouse(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        img = params["image"]
        height,width = img.shape[0],img.shape[1]

        half_width = params["p_width"]//2
        half_height = params["p_height"]//2
        corr_width = params["p_width"]%2
        corr_height = params["p_height"]%2
        
        # patch image is out of the image.
        if (x-half_width<0) or (y-half_height<0) or (x+half_width>width) or (y+half_height>height):
            img_result = cv2.drawMarker(img.copy(), (x, y), (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS, markerSize=10)
            
        # patch image is in the image.
        else:
            img_result = cv2.rectangle(img.copy(),(x-half_width,y-half_height),(x+half_width,y+half_height),(0,0,255),1) 

            # get patch image
            p_image = img[
                y-half_height : y+half_height+corr_height,
                x-half_width  : x+half_width+corr_width
                ]

            # save patch image
            save_path = save_name_generator(params["number"],params["path"])
            p_image = cv2.resize(p_image,(opt.patch_width,opt.patch_height))
            cv2.imwrite(save_path, p_image)
            print(f"saved to {save_path}")
            
            params["number"]+=1
            
        cv2.imshow(window_name, img_result)

        return 
    
def save_name_generator(number,file_path):
    """ Save a generated patch image """

    file_name,file_extension = os.path.splitext(os.path.basename(file_path))
    file_name = file_name+f"-{str(number).zfill(5)}"+file_extension
    save_path = os.path.join(opt.save_dir,file_name)
    return save_path


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Patch Image Generator')
    parser.add_argument('--dataset',  type=str, required=True, help='Path to dataset folder.')
    parser.add_argument('--save_dir', type=str, required=True, help='Path to saving folder.')
    parser.add_argument('--patch_width', type=int, default=64, help='Width of a patch image.')
    parser.add_argument('--patch_height', type=int, default=64, help='Height of a patch image.')
    parser.add_argument('--scale', type=int, default=1, help='Scale size for display.')
    opt = parser.parse_args()

    assert opt.scale>0,"Scale size must be over 0."
     
    # make save folder
    os.makedirs(opt.save_dir, exist_ok=False)

    # get image paths
    paths = sorted(glob.glob(f"{opt.dataset}/*.*"))
    len_imgs = len(paths)
    assert len_imgs>0, "Cannot find the images!!"

    # make window name
    window_name = "Patch Image Generator"

    # Patch Image Generator
    for i, path in enumerate(paths):
        """
            q or ESC: Quit
            k: Move to the next image
        """

        print(f'\n {i+1}/{len_imgs} - {path} \n')

        img = cv2.imread(path, cv2.IMREAD_COLOR)
        img = cv2.resize(img,(img.shape[1]*opt.scale, img.shape[0]*opt.scale))

        patch_width = int(opt.patch_width*opt.scale)
        patch_height = int(opt.patch_height*opt.scale)
                
        number=1
        flag = False
        while True:
            
            # show a image
            cv2.imshow(window_name, img)
    
            params = {
                "image":img.copy(),
                "path":path,
                "number":number,
                "p_width":patch_width,
                "p_height":patch_height,
            }
            
            # Click and generate patch images
            cv2.setMouseCallback(window_name, onMouse, params)
            
            # Move to next image
            if (cv2.waitKey(0) & 0xFF == ord("k")):
                break
            # Quit
            elif (cv2.waitKey(0) & 0xFF == ord("q")) or (cv2.waitKey(1) & 0xFF == 27):
                flag = True
                break
        
        # Break this loop
        if flag==True:
            break
        
    cv2.destroyAllWindows()
