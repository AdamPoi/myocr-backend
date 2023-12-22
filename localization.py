import numpy as np
import cv2
import uuid

from helper import resize_img



def localize_ktp(image):
    for iteration in range(5):
        # Removing glare
        clahed = remove_glare(image)
        # Blurring the image with a variable-sized kernel
        blur_kernel_size = (10,10)
        blur = cv2.blur(clahed, blur_kernel_size)
        # Thresholding to obtain a mask
        _, mask = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY)
        blue, green, red = cv2.split(mask)

        # Set the red and green channels to zero
        red[:], green[:] = 0, 0

        # Merge the modified channels back into an image
        blue_mask = cv2.merge([blue, green, red])
        padding = iteration * 10

        # Erosion and dilation on the mask to clean and enlarge the area
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(blue_mask, kernel, iterations=0+iteration)
        mask = cv2.dilate(blue_mask, kernel, iterations=1+iteration)

        # padded_mask = cv2.copyMakeBorder(blue_mask, 0 + padding, 0 + padding, 0 + padding, 0 + padding, cv2.BORDER_CONSTANT)
        # Edge detection using the Canny method
        lt = 50
        edges = cv2.Canny(padded_mask, lt, lt * 3)

        # Dilation and erosion on the edges to close edge lines of the card
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=2+iteration)
        edges = cv2.erode(edges, kernel, iterations=1+iteration)


        # Finding contours on the edge image
        contours, img = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        image_contour = image.copy()

        # Finding the contour with the largest area that has 4 points
        max_area = 0
        image_area = image.shape[0] * image.shape[1]
        best_rect = None

        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:
                area = cv2.contourArea(approx)
                # find biggest contour
                if area > max_area and area > image_area / 8:
                    max_area = area
                    best_rect = approx

        # If the best contour is found, break the loop
        if best_rect is not None:
            break
    
    if best_rect is None : 
      return localize_with_threshold_blue(image)

    # Drawing contours on the original image and the best contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)

    cv2.drawContours(image_contour, contours, -1, (255, 0, 0), 2)
    cv2.drawContours(image_contour, [contours[max_index]], -1, (0, 0, 255), 2)

    # Performing perspective transformation if a contour is detected
    warped = image
    if best_rect is not None:
        cv2.drawContours(image_contour, [best_rect], -1, (0, 255, 0), 2)
        warped = four_point_transform(image, best_rect.reshape(4, 2))

    return  warped

def order_points(pts):
    # Inisialisasi matriks nol untuk menyimpan 4 titik sudut hasil pengurutan
    rect = np.zeros((4, 2), dtype="float32")

    # Menghitung jumlah sumbu x dan y dari setiap titik
    s = pts.sum(axis=1)

    # Menyimpan titik dengan nilai minimum dan maksimum dari jumlah sumbu
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # Menghitung perbedaan sumbu x dan y antar titik
    diff = np.diff(pts, axis=1)

    # Menyimpan titik dengan nilai minimum dan maksimum dari perbedaan sumbu
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    ratio = 85.6 / 53.98

    if maxWidth > maxHeight:
        maxHeight = int(maxWidth / ratio)
    else:
        maxWidth = int(maxHeight * ratio)

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def remove_glare(image,clip_limit=0.5):
    # Menghapus kilau dari gambar menggunakan CLAHE (Contrast Limited Adaptive Histogram Equalization)
    result = image
    lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(12, 12))
    lab[..., 0] = clahe.apply(lab[..., 0])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return result

# Alternate four point transform 
def is_blueish(pixel, blue_threshold=127):
    blue, green, red = pixel
    return blue > green + red + blue_threshold


def threshold_blue(image, blue_threshold=127):
    blueish_mask = np.apply_along_axis(is_blueish, axis=2, arr=image, blue_threshold=blue_threshold)
    
    result_image = np.where(blueish_mask, 255, 0).astype(np.uint8)

    return result_image

def localize_with_threshold_blue(image):
  blur = cv2.blur(image, (5,5))

  mask = threshold_blue(blur)

  lt = 50
  edges = cv2.Canny(mask, lt, lt * 3)

  kernel = np.ones((5, 5), np.uint8)

  dilatation_dst = cv2.dilate(edges, kernel , iterations=4)
  erosion = cv2.erode(dilatation_dst,kernel,iterations = 3)

  edges = cv2.Canny(erosion, 50, 150)

  contours, img = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  image_contour = image.copy()

  max_area = 0
  best_rect = None

  for contour in contours:
      epsilon = 0.02 * cv2.arcLength(contour, True)
      approx = cv2.approxPolyDP(contour, epsilon, True)

      if len(approx) == 4:
          area = cv2.contourArea(approx)

          if area > max_area:
              max_area = area
              best_rect = approx

  areas = [cv2.contourArea(c) for c in contours]
  max_index = np.argmax(areas)

  warped = four_point_transform(image, best_rect.reshape(4, 2))

  return warped