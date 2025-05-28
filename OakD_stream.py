#!/usr/bin/env python3

import depthai as dai
import cv2

def main():
    # Start defining a pipeline
    pipeline = dai.Pipeline()

    # Define a source – the color camera
    cam_A = pipeline.createColorCamera()
    cam_A.setPreviewSize(640, 480)
    cam_A.setInterleaved(False)
    cam_A.setBoardSocket(dai.CameraBoardSocket.RGB)

    # Create output stream for the RGB camera
    xout = pipeline.createXLinkOut()
    xout.setStreamName("video")
    cam_A.preview.link(xout.input)

    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:
        print("OAK-D Pro camera connected. Streaming video...")

        # Output queue to receive the frames
        video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

        while True:
            in_frame = video_queue.get()
            frame = in_frame.getCvFrame()

            # Display the frame
            cv2.imshow("OAK-D Pro - RGB Stream", frame)

            # Press 'q' to quit
            if cv2.waitKey(1) == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
