import numpy as np
import cv2

from helper import resize_img



def localize_ktp(image):
    image = resize_img(image,800)
    clahed = remove_glare(image,1)

    # Mengaburkan gambar dengan kernel 10x10
    blur = cv2.blur(image, (10, 10))

    # Thresholding untuk mendapatkan masker
    _, mask = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY)

    # Erosi dan dilasi pada masker untuk membersihkan dan memperbesar area
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=5)


    # Deteksi tepi menggunakan metode Canny
    lt = 50
    edges = cv2.Canny(mask, lt, lt * 3)


    # Dilasi dan erosi pada tepi untuk menutup baris edge kartu
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=6)
    edges = cv2.erode(edges, kernel, iterations=5)

    # Menemukan kontur pada tepi gambar
    contours, img = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    image_contour = image.copy()

    # Mencari kontur dengan luas terbesar yang memiliki 4 titik
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

    # Menggambar kontur pada gambar asli dan kontur terbaik
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)

    cv2.drawContours(image_contour, contours, -1, (255, 0, 0), 2)
    cv2.drawContours(image_contour, [contours[max_index]], -1, (0, 0, 255), 2)

    # Melakukan transformasi perspektif jika kontur terdeteksi
    warped = image
    if best_rect is not None:
        cv2.drawContours(image_contour, [best_rect], -1, (0, 255, 0), 2)
        warped = four_point_transform(image, best_rect.reshape(4, 2))
    

    return (mask, edges, image_contour, warped)

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

def remove_glare(image, iteration=1):
    # Menghapus kilau dari gambar menggunakan CLAHE (Contrast Limited Adaptive Histogram Equalization)
    result = image
    for i in range(iteration):
        lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[..., 0] = clahe.apply(lab[..., 0])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return result