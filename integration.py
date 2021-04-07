import time
from datetime import datetime
import cv2
import mss
import numpy as np
import os
# import win32api, win32con
import pyautogui
import sys
import threading
from time import sleep
import math
import inference_utils
from inference_utils import *
import tensorflow as tf
import os

output_directory = os.path.abspath('inference_graph_2')
labelmap_path = os.path.abspath('labelmap.pbtxt')

model = tf.saved_model.load(output_directory)
category_index = label_map_util.create_category_index_from_labelmap(labelmap_path, use_display_name=True)

screenHeight = 1080
screenWidth = 1920

# def moveMouse(x, y):
#     win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 
#         int(x/screenWidth*65535.0), int(y/screenHeight*65535.0))


with mss.mss() as sct:
    # Use the 1st monitor
    monitor = sct.monitors[1]

    # Capture a bbox using percent values
    left = monitor["left"] + monitor["width"] * 10 // 100  # 5% from the left
    top = monitor["top"] + monitor["height"] * 23 // 100  # 5% from the top
    right = left + 330  # 400px width
    lower = top + 480  # 400px height
    bbox = (left, top, right, lower)
    count = 0
    while True:
        last_time = time.time()
        screen = np.array(sct.grab(bbox))
        screen = np.flip(screen[:, :, :3], 2) 
        # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        img = screen.copy()
        output_dict = inference_utils.run_inference_for_single_image(model, img)
        prev_x = 0
        for tensor in output_dict['detection_boxes']:
            if output_dict['detection_scores'][count] > 0.4 and ((tensor[1] * img.shape[1] - prev_x) > prev_x*0.07 or (tensor[1] * img.shape[1] - prev_x) < prev_x*0.07):
                xmin = int(tensor[1] * img.shape[1])
                ymin = int(tensor[0] * img.shape[0])
                xmax = int(tensor[3] * img.shape[1])
                ymax = int(tensor[2] * img.shape[0])
                center_x, center_y = (xmin + xmax)/2, (ymin + ymax)/2
                time.sleep(0.6)
                pyautogui.click(center_x+192,center_y+248)
                count += 1
                prev_x = center_x
                # if count == 20:
                #     time.sleep(30)


        boxes = output_dict["detection_boxes"]
        for box in boxes:
            img = cv2.rectangle(img, (int(box[0]), int(box[1]),int(box[2]), int(box[3])),(255, 0, 0),2)
        # for 
        image_np_with_detections = vis_util.visualize_boxes_and_labels_on_image_array(img, output_dict['detection_boxes'],
                              output_dict['detection_classes'],output_dict['detection_scores'], category_index, instance_masks=output_dict.get('detection_masks_reframed', None), use_normalized_coordinates=True,
                              line_thickness=8)
        # cv2.imshow('img', img)
        # cv2.imshow("img", image_np_with_detections)
        cv2.waitKey(1)
        # if cv2.waitKey(5) & 0xFF == 27:
        #     cv2.destroyAllWindows() 
        
      
quit()