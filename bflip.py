


import cv2
import numpy as np

def detect_cheating(video_path):
    cap = cv2.VideoCapture(video_path)
    
    bottle_lower = np.array([0, 100, 100], dtype=np.uint8)
    bottle_upper = np.array([10, 255, 255], dtype=np.uint8)
    
    cheating_detected = False
    frame_count = 0
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, bottle_lower, bottle_upper)
        
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            bottle_contour = max(contours, key=cv2.contourArea)
            
            x, y, w, h = cv2.boundingRect(bottle_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            bottle_area = cv2.contourArea(bottle_contour)
            if bottle_area > 1000:  
                cheating_detected = True
        
        if cheating_detected:
            cv2.putText(frame, 'Cheating Detected!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        frame_count += 1
        cv2.imshow('Frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    return cheating_detected

cheating = detect_cheating("resoucse\\bp2.mp4")#can also try with bp1
if cheating:
    print("Cheating detected!")
else:
    print("No cheating detected.")
