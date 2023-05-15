import os
import cv2
import shutil


def is_image_blurry(image_path, laplacian_threshold, tenengrad_threshold):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the Laplacian variance
    laplacian_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Calculate the Tenengrad gradient magnitude
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = cv2.magnitude(sobelx, sobely)
    tenengrad_score = cv2.mean(gradient_magnitude)[0]

    return laplacian_score < laplacian_threshold and tenengrad_score < tenengrad_threshold

def separate_images(input_folder, blurry_folder, clear_folder, laplacian_threshold, tenengrad_threshold):
    if not os.path.exists(blurry_folder):
        os.makedirs(blurry_folder)
    if not os.path.exists(clear_folder):
        os.makedirs(clear_folder)

    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        if os.path.isfile(image_path):
            if is_image_blurry(image_path, laplacian_threshold, tenengrad_threshold):
                shutil.copy(image_path, blurry_folder)
            else:
                shutil.copy(image_path, clear_folder)

# Example usage
input_folder = r"C:\Users\sombr\OneDrive - California State University, Sacramento\Desktop\AntiBlur\input_folder"
blurry_folder = r"C:\Users\sombr\OneDrive - California State University, Sacramento\Desktop\AntiBlur\blurry_folder"
clear_folder = r"C:\Users\sombr\OneDrive - California State University, Sacramento\Desktop\AntiBlur\clear_folder"
laplacian_threshold= 130
tenengrad_threshold = 1000

separate_images(input_folder, blurry_folder, clear_folder, laplacian_threshold, tenengrad_threshold)
