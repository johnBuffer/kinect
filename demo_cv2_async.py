#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np
import datetime

cv2.namedWindow('Depth')
cv2.namedWindow('RGB')
keep_running = True

def draw_canny(data):
    #gray = frame_convert2.video_cv(data)
    gray = cv2.GaussianBlur(data, (3, 3), 0)
    edged = cv2.Canny(gray, 35, 125)

    return edged

def display_depth(dev, data, timestamp):
    global keep_running
    t_start = datetime.datetime.now()
    data2 = frame_convert2.pretty_depth_cv(cv2.resize(data, (0, 0), fx=0.25, fy=0.25))
    #data2 = frame_convert2.pretty_depth_cv(data)

    #data2 = cv2.applyColorMap(data.astype(np.uint8), cv2.COLORMAP_JET)
    t_end = datetime.datetime.now()
    t_delta = t_end - t_start
    cv2.putText(data2, str(1000000/t_delta.microseconds), (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (127, 0, 0), 2)
    cv2.imshow('Depth', cv2.resize(data2, (0, 0), fx=4, fy=4))
    if cv2.waitKey(10) == 27:
        keep_running = False


def display_rgb(dev, data, timestamp):
    t_start = datetime.datetime.now()
    global keep_running


    #result = draw_canny(data)
    data = frame_convert2.video_cv(data)
    result = data.copy()

    t_end = datetime.datetime.now()
    t_delta = t_end - t_start

    cv2.putText(result, str(1000000/t_delta.microseconds), (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (127, 0, 0), 2)
    cv2.imshow('RGB', result)
    
    if cv2.waitKey(10) == 27:
        keep_running = False


def body(*args):
    if not keep_running:
        raise freenect.Kill


print('Press ESC in window to stop')
freenect.runloop(depth=display_depth,
                 video=None,
                 body=body)

freenect.runloop(depth=None,
                 video=display_rgb,
                 body=body)
