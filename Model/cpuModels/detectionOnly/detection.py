import os
from datetime import datetime
import numpy as np
import cv2 as cv
import face_recognition
import sqlite3
import json
from elasticsearch import Elasticsearch

# Connect to the Elasticsearch instance
es = Elasticsearch([{
    'scheme': 'http',       # Use 'http' since security is disabled
    'host': '127.0.0.1',    # Host is localhost (127.0.0.1)
    'port': 9200            # Default port for Elasticsearch
}])

# Define the index name for Elasticsearch
index_name = 'facial_recognition_data'

# Create the index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)



# Define paths and database connection
database_path = "facial_analysis/DataBase/user_database.db"
known_face_encodings = np.load('known_face_encodings.npy')
known_face_names = np.load('known_face_names.npy')

conn = sqlite3.connect(database_path)
c = conn.cursor()

video_capture = cv.VideoCapture(0)

recognized_users = []
output_file = "facial_analysis/recognized_users_report.json"

while True:
    isTrue, frame = video_capture.read()

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            # Retrieve user data from the database
            c.execute("SELECT * FROM user_info WHERE firstname = ?", (name,))
            user_data = c.fetchone()
            if user_data:
                user_id, firstname, lastname, phone, sex, emergency_contact, division, image_paths_str = user_data
                
                # Prepare user data for JSON report
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user = {
                    'firstname': firstname,
                    'lastname': lastname,
                    'phone': phone,
                    'sex': sex,
                    'emergency_contact': emergency_contact,
                    'division': division,
                    'timestamp': timestamp
                }
                
                # Add to recognized_users list if not already added
                if not any(u['firstname'] == firstname and u['lastname'] == lastname for u in recognized_users):
                    recognized_users.append(user)

                    # Update JSON file immediately
                    with open(output_file, 'w') as f:
                        json.dump(recognized_users, f, indent=4)
                    print(f"Updated report saved to {output_file}")

                    # Load the updated data into Elasticsearch
                    es.index(index=index_name, body=user)
                    print(f"Data for {firstname} {lastname} indexed to Elasticsearch.")

        cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        label_text = name
        label_size, _ = cv.getTextSize(label_text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)
        label_width, label_height = label_size
        label_x = left
        label_y = top - 12 if top - 12 > 0 else top + 12
        cv.rectangle(frame, (label_x - 2, label_y - 2), (label_x + label_width + 2, label_y + label_height + 2), (0, 255, 0), -1)
        cv.putText(frame, label_text, (label_x, label_y + label_height), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv.imshow("Video", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv.destroyAllWindows()
conn.close()
