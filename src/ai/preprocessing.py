import numpy as np
import cv2


def denoise(image_url, output_url):
    imga = cv2.imread(image_url, 0)

    img = 255 - np.uint8(imga)
    kernel = np.ones((3, 3), np.uint8)

    # image1 = cv2.erode(img, kernel) 
    image = cv2.erode(img, kernel) 

    data = 255 - np.uint8(image)
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    image_sharp = cv2.filter2D(src=data, ddepth=-1, kernel=kernel)

    cv2.imwrite(output_url, image_sharp)
    return output_url
