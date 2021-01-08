import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui as pa

# draws line on an image
def draw_lines(img, lines):
    try:
        for line in lines:
            for x0, y0, x1, y1 in line:
                cv2.line(img, (x0, y0), (x1, y1), [0, 255, 0], thickness=3)
    except:
        pass
    return img


# to give us time to get to the game and unpause the game
def start_countdown(seconds):
    for i in range(seconds):
        print(i + 1)
        time.sleep(1)


def roi(img, verticies):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, verticies, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_image(original_image):
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    verticies = np.array(
        [[0, 500], [0, 250], [200, 240], [600, 240], [800, 250], [800, 500]]
    )

    processed_image = roi(processed_image, [verticies])
    processed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)

    lines = cv2.HoughLinesP(processed_image, 1, np.pi / 180, 180, np.array([]), 250, 2)
    processed_image = draw_lines(original_image, lines)
    return processed_image


# capture the image!
last_time = time.time()
while True:
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
    print("loop took {} seconds".format(time.time() - last_time))
    last_time = time.time()
    cv2.imshow("game", process_image(screen))

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
