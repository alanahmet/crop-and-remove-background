from rembg import remove
import argparse
from detect import detect 
import torch
from utils.general import strip_optimizer
import os
#!python remove.py --weights yolov7.pt --conf 0.25 --img-size 640 --source inference/images/image1.jpg --crop True


if __name__ == '__main__':
    """
    Main function to run object detection and background removal on images.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov7.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='inference/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--no-trace', action='store_true', help='don`t trace model')

    parser.add_argument('--crop', type=str, default="False", choices=["True", "False"], help='crop the image')
    parser.add_argument('--boundbox', type=str, default="True", choices=["True", "False"], help='dont crate bb')
    opt = parser.parse_args()
    print(opt)
    #check_requirements(exclude=('pycocotools', 'thop'))
    
    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov7.pt']:
                detect(opt)
                strip_optimizer(opt.weights)
        else:
            detect(opt)
    if opt.crop == "True":
        input_folder = 'runs/cropped/'
        input_path = input_folder + list(sorted(os.listdir(input_folder)))[-1]
        output_path = 'runs/background-removed/' + list(sorted(os.listdir(input_folder)))[-1]
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        for file in os.listdir(input_path):
            print(file)
            with open(input_path +"/"+ file, 'rb') as i:
                with open(output_path +"/"+ file, 'wb') as o:
                    input = i.read()
                    output = remove(input)
                    o.write(output)