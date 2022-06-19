import cv2
import numpy as np


def nothing(x):
    pass


def setup() -> None:
    cv2.namedWindow('Webcam')
    cv2.namedWindow('ChromaKeyControlWindow')
    cv2.createTrackbar('UpperR', 'ChromaKeyControlWindow', 0, 255, nothing)
    cv2.createTrackbar('UpperG', 'ChromaKeyControlWindow', 0, 255, nothing)
    cv2.createTrackbar('UpperB', 'ChromaKeyControlWindow', 0, 255, nothing)
    cv2.createTrackbar('LowerR', 'ChromaKeyControlWindow', 0, 255, nothing)
    cv2.createTrackbar('LowerG', 'ChromaKeyControlWindow', 0, 255, nothing)
    cv2.createTrackbar('LowerB', 'ChromaKeyControlWindow', 0, 255, nothing)


def main() -> None:
    video = cv2.VideoCapture(2)
    setup()
    while True:
        _, frame = video.read()
        # resizing the frame to 720p and invert on X-axi
        frame = cv2.resize(frame, (1280, 720))
        frame = np.fliplr(frame)
        # getting the upper and lower chromakey from GUI
        upper_chroma_key_r = cv2.getTrackbarPos('UpperR', 'ChromaKeyControlWindow')
        upper_chroma_key_g = cv2.getTrackbarPos('UpperG', 'ChromaKeyControlWindow')
        upper_chroma_key_b = cv2.getTrackbarPos('UpperB', 'ChromaKeyControlWindow')
        lower_chroma_key_r = cv2.getTrackbarPos('LowerR', 'ChromaKeyControlWindow')
        lower_chroma_key_g = cv2.getTrackbarPos('LowerG', 'ChromaKeyControlWindow')
        lower_chroma_key_b = cv2.getTrackbarPos('LowerB', 'ChromaKeyControlWindow')
        # create color pixel for both
        lower = np.array([lower_chroma_key_b, lower_chroma_key_g, lower_chroma_key_r])
        upper = np.array([upper_chroma_key_b, upper_chroma_key_g, upper_chroma_key_r])
        # create the chromakey filter
        mask = cv2.inRange(frame, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        # load background image, resize it
        background_image = cv2.imread('images/room.png')
        background_image = cv2.resize(background_image, (1280, 720))
        # remove the chromakey color
        final_frame = frame - result
        # replace the chromakey color pixel to the respective background pixel
        final_frame = np.where(final_frame == 0, background_image, final_frame)
        # show the final frame on the Webcam window
        cv2.imshow('Webcam', final_frame)
        # waiting for interrupt key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
