import cv2

#ADDITIONAL FUNCTIONS
def transparent_circle(frame,center,radius,color, alpha = 0.5):
    overlay = frame.copy()
    
    cv2.circle(overlay, center, radius, color, -1)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame

def transparent_sector(frame,center,radius,color,angle_start,divisions,alpha = 0.5,thickness=5):
    overlay = frame.copy()
    
    cv2.ellipse(overlay, center, (radius,radius), 0, angle_start, angle_start + (360//divisions) , color, thickness)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame


def transparent_circle_boundary(frame,center,radius,color, alpha = 0.5,boundary=5):
    overlay = frame.copy()
    
    cv2.circle(overlay, center, radius, color, boundary)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame