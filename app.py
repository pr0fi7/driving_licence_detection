import threading
import cv2
import streamlit as st
from matplotlib import pyplot as plt
from streamlit_webrtc import webrtc_streamer, WebRtcMode, VideoProcessorBase

# Thread-safe image container
lock = threading.Lock()
img_container = {"img": None}

# Custom Video Processor Class
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.img_container = img_container

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        with lock:
            self.img_container["img"] = img
        return frame

# Streamlit Interface
st.title("Video Recording and Processing Application")
st.write("This application allows you to record a video and then processes it using a custom API.")

# Video Streamer
ctx = webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# Placeholder for Matplotlib Figure
fig_place = st.empty()
fig, ax = plt.subplots(1, 1)

# Video Processing Loop
while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue

    # Convert the image to grayscale and display histogram
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ax.cla()
    ax.hist(gray.ravel(), 256, [0, 256])
    fig_place.pyplot(fig)

    # Add your custom API call here to process the image or video frame
    # processed_data = my_custom_api_process(img)
    # st.write(processed_data)

# Add a button to stop the video stream and save the recording
if st.button("Stop Recording and Process Video"):
    if img_container["img"] is not None:
        # You can add code here to handle the video processing with your custom API
        st.write("Processing video...")
        st.video(img_container["img"])
    else:
        st.warning("No video recorded yet.")
