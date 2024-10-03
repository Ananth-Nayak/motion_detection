import cv2, time
from datetime import datetime
import pandas as pd


first_frame = None
video = cv2.VideoCapture(0)
status_list = [None,None]
times = []   

while True:
    check, frame = video.read()
    status = 0 #this variable is used to find the timings object motion
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # using gausian blur to make image smooth which reduces the noise and increase the accuracy of calculation
    gray = cv2.GaussianBlur(gray,(21,21),0)
 
    if first_frame is None:           
        first_frame = gray
        continue       
        # first frame should always be a static to detect the motion
        # assigning gray to first frame when the first frame is none     
    

    # taking difference of current frame and first frame to find the difference in intensity
    # to detect the object
    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_delta = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    #the above code uses delta frame and wherever the difference is more than 30 
    # it puts white intesity there (255)
    # since it returns tuple, we require only first element of tuple.

    # to dilate or to smooth image we use cv2.dilate method
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=2)
    # iterations means how many time should we go through the image to make it smooth


    # finding contours
    (conts,_) = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in conts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1 # when the object is detected changing to 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

    status_list=status_list[-2:]

    status_list.append(status)  # to store whether object is in motion or not (0,1)
    if status_list[-2] == 0 and status_list[-1] == 1: # when status changes to 0 to 1 means object started to motion
        times.append(datetime.now())              # we are recording that time
    if status_list[-2] == 1 and status_list[-1] == 0:  # when it is 0 to 1 object motion is ended
        times.append(datetime.now())  

    
    cv2.imshow("Gray image",gray)
    cv2.imshow("Delta frame",delta_frame)
    cv2.imshow("Threshold frame",thresh_delta)
    cv2.imshow("Color frame",frame)


    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())  # if we close the capturing video before motion of obj is ended
        break                                  # we store the time when we stop the video

# while loop ends

#creating list of dictionaries
data = [{"Start":times[i],"End":times[i+1]} for i in range(0,len(times),2)]

# creating a data frame using list of dictionaries
df = pd.DataFrame(data)

df.to_csv("times.csv")

video.release()
cv2.destroyAllWindows()