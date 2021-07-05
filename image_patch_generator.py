import cv2
import glob
import os
import argparse

def launch_animation():
    try:
        filepath = 'gif.gif'
        cap = cv2.VideoCapture(filepath)

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                cv2.imshow("Frame", frame)
                cv2.moveWindow("Frame", 0,0) # Window表示位置指定
                cv2.waitKey(1)
            else:
                cap.release()
        cv2.destroyAllWindows()
    except:
        print("skipped launch_animation.")

def onMouse(event, x, y, flags, params):
    # パッチ画像の領域描画
    # 保存
    # パッチ画像の領域削除

    if event == cv2.EVENT_LBUTTONDOWN:
        img = params["image"]
        height,width = img.shape[0],img.shape[1]
        
        # 指定領域が画像をはみ出ている
        if (x-p_half<0) or (y-p_half<0) or (x+p_half>width) or (y+p_half>height):
            img_result = cv2.drawMarker(img.copy(), (x, y), (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS, markerSize=10)
            print("指定した領域が画像領域からはみ出しています。") # print("The specified area extends beyond the image area.")
            
        # 指定領域が画像内に収まっている
        else:
            # 指定領域の描画
            img_result = cv2.rectangle(img.copy(),(x-p_half,y-p_half),(x+p_half,y+p_half),(0,0,255),2) 

            # パッチ画像の取得
            p_image = img[y-p_half:y+p_half,x-p_half:x+p_half]
            p_width, p_height = p_image.shape[0],p_image.shape[1]  
            
            # パッチ画像の描画
            margin = 10
            img_result[margin:p_width+margin,margin:p_height+margin] = p_image
            img_result = cv2.rectangle(img_result,(margin,margin),(p_width+margin,p_height+margin),(0,0,255),1)
            
            # パッチ画像の保存
            save_path = save_name_generator(params["number"],params["path"])
            cv2.imwrite(save_path, p_image)
            print(f"saved to {save_path}")
            params["number"]+=1
            

        # 1秒間パッチ画像領域を表示
        cv2.imshow(window_name, img_result)
        # 1秒間パッチ画像を表示
        cv2.waitKey(1000)
        cv2.imshow(window_name, img)

        return print("saving is complete.")
    
def save_name_generator(number,file_path):
    file_name,file_extension = os.path.splitext(os.path.basename(file_path))
    file_name = file_name+f"-{number}"+file_extension
    save_path = os.path.join(opt.save,file_name)
    return save_path
    

if __name__ == "__main__":
    launch_animation()

    parser = argparse.ArgumentParser(description='Patch Image Generator')
    parser.add_argument('--dataset',  type=str, required=True, help='Path to dataset folder.')
    parser.add_argument('--save', type=str, required=True, help='Path to saving folder.')
    parser.add_argument('--patch_size', type=int, default=64, help='Size of a patch image.')
    opt = parser.parse_args()

     
    # 今回はパッチ画像は正方形に限定する. 
    os.makedirs(opt.save, exist_ok=True)

    # 画像パス
    paths = sorted(glob.glob(f"{opt.dataset}/*"))
    len_imgs = len(paths)

    # パッチ画像サイズ
    p_side = opt.patch_size
    p_half = int(p_side//2)

    
    for i, path in enumerate(paths):
        window_name = "Patch Image Generator"
        flag = False
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        
        print("=========================")
        print(f'Image - {i+1}/{len_imgs}')
        print("=========================")
        
        number=1
        while True:
            # q or ESC: 終了
            # k: 次
            
            # 画像の表示
            cv2.imshow(window_name, img)
            cv2.moveWindow(window_name, 80,80) # Window表示位置指定
                
            params = {
                "image":img,
                "path":path,
                "number":number,
            }
            
            # クリック & パッチ画像の生成
            cv2.setMouseCallback(window_name, onMouse, params)
            
            # 次の画像
            if (cv2.waitKey(0) & 0xFF == ord("k")):
                print("k is clicked.")
                break
            # 終了
            elif (cv2.waitKey(0) & 0xFF == ord("q")) or (cv2.waitKey(1) & 0xFF == 27):
                print("q is clicked.")
                flag = True
                break
        
        # 終了
        if flag==True:
            print("break loop.")
            break
        
    cv2.destroyAllWindows()
