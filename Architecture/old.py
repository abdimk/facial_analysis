#library versions 
#opencv-python 4.8.1.78  // pip install opencv-python
#numpy  1.24.2
#face-recognition 1.3.0 pip install face-recognition



import cv2 as cv
import face_recognition

#Load the know face encodings and names 
known_face_encodings = []
known_face_names = []


#Load the known faces and thier names 
known_person1_image = face_recognition.load_image_file('person1.jpg') ##put full image path
known_person2_image = face_recognition.load_image_file('person2.jpg')
known_person3_image = face_recognition.load_image_file('person3.jpg')



known_person1_encoding = face_recognition.face_encoding(known_person1_image)[0]
known_person2_encoding = face_recognition.face_encoding(known_person2_image)[0]
known_person3_encoding = face_recognition.face_encoding(known_person3_image)[0]



known_face_encodings.append(known_person1_encoding)
known_face_encodings.append(known_person2_encoding)
known_face_encodings.append(known_person3_encoding)



known_face_names.append("Person1")
known_face_names.append("Person2")
known_face_names.append("Person3")




#Initalize the webcam

video_capture = cv.VideoCapture(0)


while True:
    isTrue,frame = video_capture.read()

    #find all face locations in the current frame 
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    #Loop through eeach face found int the frame

    for(top,right,bottom,left), face_encoding in zip(face_locations, face_encodings):
        #check if the face matches any known face
        matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
        name = "Unknown"


        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]


        #Draw a box around the faces and label with the names
        cv.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
        cv.putText(frame,name(left,top -10),cv.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),2)


    #Display the resulting frame
    cv.imshow("Video",frame)

    if cv.waitKey(1) & 0xFF==ord('q'):
        break


video_capture.release()
cv.destroyAllWindows()


