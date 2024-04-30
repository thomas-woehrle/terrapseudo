import cv2
import numpy as np


def process_image(path_to_image):
    # Image is loaded in BGR format as np array
    image = cv2.imread(path_to_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # clipping to 320/224 ratio
    # cutting of 96 from left, right and 10 from top, bottom -> 640x448 dimension*
    image = image[10:448+10, 96:640+96]
    # then downsample
    image = cv2.resize(image, (320, 224), interpolation=cv2.INTER_AREA)

    data = np.divide(image, 255)

    # ImageNet normalization
    data[:, :, 0] = (data[:, :, 0]-0.485)/0.229
    data[:, :, 1] = (data[:, :, 1]-0.456)/0.224
    data[:, :, 2] = (data[:, :, 2]-0.406)/0.225
    data = np.expand_dims(data, axis=0)
    data = np.transpose(data, axes=[0, 3, 1, 2]).astype(np.float32)

    return data, image
