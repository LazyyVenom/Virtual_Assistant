import cv2
import random

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


def transparent_line(frame,p1,p2,color,thickness,alpha):
    overlay = frame.copy()

    cv2.line(overlay,p1,p2,color,thickness)

    cv2.addWeighted(overlay,alpha,frame,1-alpha,0,frame)

    return frame


def transparent_circle_boundary(frame,center,radius,color, alpha = 0.5,boundary=5):
    overlay = frame.copy()
    
    cv2.circle(overlay, center, radius, color, boundary)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame


def show_random_numbers_on_frame(frame, num_numbers, color=(255, 210, 0)):
    older_frame = frame.copy()

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 2
    
    frame_height, frame_width, _ = frame.shape
    
    for _ in range(num_numbers):
        number = random.randint(99,999)
        x = random.randint(0, frame_width - 50)
        y = random.randint(50, frame_height)
        cv2.putText(frame, str(number), (x, y), font, font_scale, color, thickness, cv2.LINE_AA)
    
    blended_frame = cv2.addWeighted(older_frame, 0.6, frame, 0.4, 0)

    return blended_frame


def option_generator(frame,center: tuple,text: str,radius: int,color: tuple=(255, 210, 0)):
    frame = transparent_circle(frame,center,radius,color)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    cv2.putText(frame, text, (center[0]-10, center[1]+10), font, font_scale, (200, 130, 0), thickness, cv2.LINE_AA)
    return frame
    