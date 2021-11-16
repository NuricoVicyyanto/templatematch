import cv2
import numpy as np

cap = cv2.VideoCapture(0)
template = cv2.imread("ssd2.jpg", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.8)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0]+w, pt[1]+h), (0,255,0), 3)

    cv2.imshow("Template Matching", frame)

    if(cv2.waitKey(5) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()