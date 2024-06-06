import cv2
import numpy as np

lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

cap = cv2.VideoCapture("resource\\v.mp4")

previous_centers = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            
            previous_centers.append((cx, cy))
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            
            if len(previous_centers) > 2:
                (x1, y1) = previous_centers[-2]
                (x2, y2) = previous_centers[-1]
                
                vx = x2 - x1
                vy = y2 - y1
                
                predicted_x = x2 + 2 * vx
                predicted_y = y2 + 2 * vy
                
                cv2.circle(frame, (predicted_x, predicted_y), 5, (255, 0, 0), -1)
    
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(250) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
