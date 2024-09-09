import os
import numpy as np
import cv2 as cv
import face_recognition
import sqlite3

database_path = "/home/ephi471/Desktop/facial_analysis/DataBase/user_database.db"

known_face_encodings = []
known_face_names = []

conn = sqlite3.connect(database_path)
c = conn.cursor()

c.execute("SELECT firstname, image FROM user_info")
user_info = c.fetchall()

for firstname, image_paths_str in user_info:
    image_paths = image_paths_str.split(',')
    for image_path in image_paths:
        person_image = face_recognition.load_image_file(image_path)
        person_encoding = face_recognition.face_encodings(person_image)

        if person_encoding:
            known_face_encodings.append(person_encoding[0])
            known_face_names.append(firstname)

np.save('known_face_encodings.npy', known_face_encodings)
np.save('known_face_names.npy', known_face_names)

print("Encoding complete. Saved to files.")

conn.close()
