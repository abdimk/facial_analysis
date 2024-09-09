#default
#library versions 
#opencv-python 4.8.1.78  // pip install opencv-python
#numpy  1.24.2
#face-recognition 1.3.0 pip install face-recognition

#This works by loading the known images and folder name from the path defined bellow

import os
import numpy as np
import cv2 as cv
import face_recognition
#from ...Kafka import cls
#from kafka import KafkaConsumer


# Initialize the known face encodings and names lists
known_face_encodings = []
known_face_names = []


# Path to the database folder containing subfolders for each person
database_path = "../../DataBase/userdb"


for person_name in os.listdir(database_path):
    person_folder = os.path.join(database_path, person_name)

   
    if os.path.isdir(person_folder):
        # Loop over each image file in the person's folder
        for image_name in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_name)
            
            # Load the image and encode the face
            person_image = face_recognition.load_image_file(image_path)
            person_encoding = face_recognition.face_encodings(person_image)

            # Some images may not contain faces; skip those
            if person_encoding:
                known_face_encodings.append(person_encoding[0])
                known_face_names.append(person_name)


# # Initialize the webcam
video_capture = cv.VideoCapture(0)

#consumer = KafkaConsumer(cls.name, cls.bootstrap_servers)



while True:
    #for message in consumer:
    #p_arr = np.frombuffer(message.value, np.uint8)
    #frame = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    isTrue, frame = video_capture.read()

    
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
       
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv.putText(frame, name, (left, top - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    
    cv.imshow("Video", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

#video_capture.release()
cv.destroyAllWindows()