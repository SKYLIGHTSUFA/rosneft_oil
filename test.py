import cv2


image = cv2.imread("img.png")

w, h, _ = image.shape

stride = h//3 - 1
print(w,h, stride)
for i in range(3):
    cv2.imwrite(f"{i}.jpg", cv2.rotate(cv2.resize(image[:, i*stride:(i+1)*stride], (w,h)), cv2.ROTATE_90_CLOCKWISE))