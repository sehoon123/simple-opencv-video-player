import cv2 as cv
import urllib.request
import ssl
import numpy as np


# Define a function to play videos
def play_video(video_file):
    # Check if video file is a URL
    if video_file.startswith('http://') or video_file.startswith('https://'):
        # Create a custom SSL context that does not verify the certificate
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Download the video file and save it to a temporary file
        with urllib.request.urlopen(video_file, context=ssl_context) as response:
            with open('temp.mp4', 'wb') as f:
                f.write(response.read())
        video_file = 'temp.mp4'

    # Read the given video file
    cap = cv.VideoCapture(video_file)

    fps = cap.get(cv.CAP_PROP_FPS)
    if fps == 0:
        fps = 30  # set default FPS value
    wait_msec = int(1 / fps * 1000)

    frame_total = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    frame_shift = 10
    speed_table = [1 / 10, 1 / 8, 1 / 4, 1 / 2, 1, 2, 3, 4, 5, 8, 10]
    speed_index = 4
    volume = 0.5  # initial volume

    while True:
        valid, img = cap.read()
        if not valid:
            break

        # Show the image
        frame = int(cap.get(cv.CAP_PROP_POS_FRAMES))
        info = f'Frame: {frame}/{frame_total}, Speed: x{speed_table[speed_index]:.2g}, Volume: {volume:.2g}'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
        cv.imshow('Video Player', img)

        # Process the key event
        key = cv.waitKey(max(int(wait_msec / speed_table[speed_index]), 1))
        if key == ord(' '):
            key = cv.waitKey()
        if key == 27: # ESC
            break
        elif key == ord('\t'):
            speed_index = 4
        elif key == ord('>') or key == ord('.'):
            speed_index = min(speed_index + 1, len(speed_table) - 1)
        elif key == ord('<') or key == ord(','):
            speed_index = max(speed_index - 1, 0)
        elif key == ord(']') or key == ord('}'):
            cap.set(cv.CAP_PROP_POS_FRAMES, frame + frame_shift)
        elif key == ord('[') or key == ord('{'):
            cap.set(cv.CAP_PROP_POS_FRAMES, max(frame - frame_shift, 0))
        elif key == ord('='):
            volume = min(volume + 0.1, 1.0)
            audio = np.zeros((200,200,3), np.uint8)
            audio[:, :int(volume*200), :] = (0,255,0)
            cv.imshow('Audio', audio)
        elif key == ord('-'):
            volume = max(volume - 0.1, 0.0)
            audio = np.zeros((200,200,3), np.uint8)
            audio[:, :int(volume*200), :] = (0,255,0)
            cv.imshow('Audio', audio)
        elif key == ord('s'):  # Press 's' to capture screen
            ret, frame = cap.read()
            if ret:
                # Save the captured frame to a file
                frame_number = int(cap.get(cv.CAP_PROP_POS_FRAMES))
                filename = f"caputres/capture_{frame_number:03}.png"
                success = cv.imwrite(filename, frame)
                if success:
                    print(f"Screen captured to {filename}")
                else:
                    print("Error: failed to save screen capture to file.")
            else:
                print("Error: failed to capture screen.")


    cap.release()
    cv.destroyAllWindows()

# Test the function with a video file
video_file = 'MVI_2350.mov'
# play_video(video_file)

# Test the function with a URL
url = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'
play_video(url)