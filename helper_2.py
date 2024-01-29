from ultralytics import YOLO
import time
import streamlit as st
import cv2
from pytube import YouTube
import os

import settings
import numpy as np
import pyautogui

import mailing_service


def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


# def display_tracker_options():
#     display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
#     is_display_tracker = True if display_tracker == 'Yes' else False
#     if is_display_tracker:
#         tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
#         return is_display_tracker, tracker_type
#     return is_display_tracker, None

def detectingimg_count(count, res):
    print("res start!!!")
    for r in res :
        
        print("------")
        folder_dir = './hornet_image'
        
        bees = r.boxes.cls.tolist()
        print(set(bees))
        
        #말벌이 하나라도 있으면 카운트 +1
        for bee in set(bees):  
            if int(bee) ==1:
                count += 1
                print("fuck the hornet")
        
        #말벌 이미지 저장하기 
        file_name = folder_dir+ f'/hornet_{count:04d}.png'
        os.makedirs(folder_dir, exist_ok = True)
        cv2.imwrite(file_name,r.orig_img)

        print("------")
            
    print("res finish!!")
    return count, file_name


def _display_detected_frames(conf, model, st_frame, image,count):
    """
    Display the detected objects on a video frame using the YOLOv8 model.

    Args:
    - conf (float): Confidence threshold for object detection.
    - model (YoloV8): A YOLOv8 object detection model.
    - st_frame (Streamlit object): A Streamlit object to display the detected video.
    - image (numpy array): A numpy array representing the video frame.
    - is_display_tracking (bool): A flag indicating whether to display object tracking (default=None).

    Returns:
    None
    """

    # Resize the image to a standard size
    

    # Display object tracking, if specified
    
    # image size predict 
    # Predict the objects in the image using the YOLOv8 model
    res = model.predict(image,imgsz=(1088,1920),
            vid_stride=5, half=True, conf=conf)
    #mailing_service.mail_send(res=res)
    #print('mail sending---!!!!')
    
    count, file_name = detectingimg_count(count, res)
    
    # # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_image = st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )
    
    return count,file_name
    


def play_youtube_video(conf, model):
    """
    Plays a webcam stream. Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_youtube = st.sidebar.text_input("YouTube Video url")

    # is_display_tracker, tracker = display_tracker_options()

    if st.sidebar.button('Detect Objects'):
        try:
            yt = YouTube(source_youtube)
            stream = yt.streams.filter(file_extension="mp4", res=720).first()
            vid_cap = cv2.VideoCapture(stream.url)

            st_frame = st.empty()
            count = 0
            mail_count = 0
            first_send_time = time.time()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    count,file_name = _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             count
                                             )
                    print("goood job boy!!")
                    print(count)
                    # count = count1
                    count, mail_count,first_send_time = mailing_service.Requirements_sending_mail(count,
                                                                                       mail_count, 
                                                                                       file_name,
                                                                                       first_send_time)
                    
                   
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))


# def play_rtsp_stream(conf, model):
#     """
#     Plays an rtsp stream. Detects Objects in real-time using the YOLOv8 object detection model.

#     Parameters:
#         conf: Confidence of YOLOv8 model.
#         model: An instance of the `YOLOv8` class containing the YOLOv8 model.

#     Returns:
#         None

#     Raises:
#         None
#     """
#     source_rtsp = st.sidebar.text_input("rtsp stream url:")
#     st.sidebar.caption('Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
#     # is_display_tracker, tracker = display_tracker_options()
#     if st.sidebar.button('Detect Objects'):
#         try:
#             vid_cap = cv2.VideoCapture(source_rtsp)
#             st_frame = st.empty()
#             count = 0
#             while (vid_cap.isOpened()):
#                 success, image = vid_cap.read()
#                 if success:
#                      _display_detected_frames(conf,
#                                               model,
#                                               st_frame,
#                                               image, 
#                                               count
#                                               )
                  
#                 else:
#                     vid_cap.release()
#                     break
#         except Exception as e:
#             vid_cap.release()
#             st.sidebar.error("Error loading RTSP stream: " + str(e))


def play_webcam(conf, model):
    """
    Plays a webcam stream. Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_webcam = settings.WEBCAM_PATH
    # is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            count = 0
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             count
                                             )
                    
                    
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))
def play_rtsp_stream(conf, model):
 
    while True:
        # Capture the screen content
        screen = np.array(pyautogui.screenshot(region=(0, 0, 640, 480)))
        frame = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
 
        # Run YOLOv8 inference on the frame
        results = model(frame)
 
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
 
        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)
 
 
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
 
    # Close all windows
    cv2.destroyAllWindows()

def play_stored_video(conf, model):
    """
    Plays a stored video file. Tracks and detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_vid = st.sidebar.selectbox(
        "Choose a video...", settings.VIDEOS_DICT.keys())

    # is_display_tracker, tracker = display_tracker_options()

    with open(settings.VIDEOS_DICT.get(source_vid), 'rb') as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)

    if st.sidebar.button('Detect Video Objects'):
        try:
            vid_cap = cv2.VideoCapture(
                str(settings.VIDEOS_DICT.get(source_vid)))
            st_frame = st.empty()
            count = 0
            mail_count = 0
            first_send_time = time.time()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    count,file_name =_display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             count
                                             )
                    print("goood job boy!!")
                    print(count)
                    
                    count, mail_count,first_send_time = mailing_service.Requirements_sending_mail(count,
                                                                                       mail_count, 
                                                                                       file_name,
                                                                                       first_send_time)
                    
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))
