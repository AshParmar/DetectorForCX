import cv2
from io import BytesIO
import numpy as np
def process_image(image_file):
    #BytesIO object to hold image data
    in_memory_file = BytesIO()
    image_file.save(in_memory_file)

    images_bytes=in_memory_file.getvalue()
    #Convert bytes data to numpy array
    nparr = np.frombuffer(images_bytes, np.uint8)
    #Decode numpy array to OpenCV image
    img =cv2.imdecode(nparr, cv2.IMREAD_COLOR )
    #BGR to Grayscale conversion
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces=face_cascade.detectMultiScale(gray,1.1,4)
    if len(faces)==0:
        return images_bytes,None
    
    #finding largest face with width and height
    largest_face=max(faces, key=lambda r:r[2]*r[3])

    (x,y,w,h)=largest_face

    cv2.rectangle(img, (x,y), 
                  (x+w, y+h), 
                  (255,0,0), 3)
    is_succes , buffer=cv2.imencode('.jpg',img)

    return buffer.tobytes(), largest_face