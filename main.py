import cv2
import pytesseract

from utils import resize_image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

"""
Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
                        bypassing hacks that are Tesseract-specific.
"""


image = cv2.imread('./img/tesco_01.jpg')
image = resize_image(image, scale_percent=100)


def find_words(img, draw=False):
    # finding words is good for drawing squares, but the actual OCR is terrible
    config = r'--oem 2 --psm 6'
    data = pytesseract.image_to_data(img, config=config).splitlines()
    words = []
    for i, d in enumerate(data):
        d = d.split('\t')
        if i == 0 or int(d[10]) == -1 or len(d) == 11:
            continue
        x, y, w, h = int(d[6]), int(d[7]), int(d[8]), int(d[9])

        # detect row
        leeway = 2
        prev_y = int(data[i-1].split('\t')[7])

        if prev_y-leeway <= y <= prev_y+leeway:
            print(d[11])

        if draw:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(img, (x, y-leeway), (x + w, y + h + leeway), (255, 0, 0), 1)

        crop_img = img[y-10:y + h + 10, x-10:x + w + 10]

    halfway_x = int(img.shape[1]/2)
    cv2.line(img, (halfway_x, 0), (halfway_x, img.shape[0]), (0, 255, 255), 1)


def find_chars(img):
    config = r'--oem 3 --psm 8'
    height, width, _ = img.shape
    boxes = pytesseract.image_to_boxes(img, config=config)
    word = ''
    for b in boxes.splitlines():
        b = b.split(' ')
        word += b[0]
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, height-y), (w, height-h), (0, 0, 255), 1)
        cv2.putText(img, b[0], (x, height-y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 1)
    print(word)



find_words(image, draw=True)
cv2.imshow('Main Image', image)
cv2.waitKey(0)