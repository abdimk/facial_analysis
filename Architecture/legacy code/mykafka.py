import os
import cv2 as cv
import numpy as np
import face_recognition
import sqlite3
import json
import csv
from elasticsearch import Elasticsearch
import shutil
import threading
from kafka import KafkaConsumer
from queue import Queue
from datetime import datetime

# Flag to control the timer
continue_archiving = True

es = Elasticsearch([{'scheme': 'http', 'host': 'localhost', 'port': 9200}])

# Define the index name for Elasticsearch
index_name = 'facial_recognition_data'

def clear_elasticsearch_index():
    try:
        es.indices.delete(index=index_name, ignore=[400, 404])
        es.indices.create(index=index_name)
        print(f"Cleared and recreated index: {index_name}")
    except Exception as e:
        print(f"Error clearing index: {e}")

# Function to archive CSV and reset JSON data every 40 seconds
def archive_and_reset_json_file():
    if not continue_archiving:
        return

    if recognized_users:
        archive_dir = "/home/ephi471/Desktop/facial_analysis/historical_reports/"
        os.makedirs(archive_dir, exist_ok=True)

        # Generate a new file name with a timestamp for the CSV report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"recognized_users_report_{timestamp}.csv"
        new_filepath = os.path.join(archive_dir, new_filename)

        # Retrieve all users from the database
        c.execute("SELECT * FROM user_info")
        all_users = c.fetchall()

        # Write the CSV file
        with open(new_filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Firstname', 'Lastname', 'Phone', 'Sex', 'Emergency Contact', 'Division', 'Recognized'])

            for user_data in all_users:
                user_id, firstname, lastname, phone, sex, emergency_contact, division, image_paths_str = user_data
                recognized = 'Yes' if any(u['firstname'] == firstname and u['lastname'] == lastname for u in recognized_users) else 'No'
                writer.writerow([firstname, lastname, phone, sex, emergency_contact, division, recognized])

        print(f"Archived CSV report saved to {new_filepath}")

    clear_elasticsearch_index()
    recognized_users.clear()
    with open(output_file, 'w') as f:
        json.dump(recognized_users, f, indent=4)
    print(f"Reset report at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    threading.Timer(40, archive_and_reset_json_file).start()

# Database and models
database_path = "/home/ephi471/Desktop/facial_analysis/DataBase/user_database.db"
known_face_encodings = np.load('/home/ephi471/Desktop/facial_analysis/Model/known_face_encodings.npy')
known_face_names = np.load('/home/ephi471/Desktop/facial_analysis/Model/known_face_names.npy')

conn = sqlite3.connect(database_path, check_same_thread=False)
c = conn.cursor()

# Kafka consumer setup
frame_queue = Queue(maxsize=1)  # Limit the queue size to 1 frame

def consume_frames():
    consumer = KafkaConsumer('video-stream',
                             bootstrap_servers='localhost:9092',
                             auto_offset_reset='latest',
                             fetch_max_bytes=1048576,
                             max_poll_records=100)
    while True:
        try:
            for message in consumer:
                np_arr = np.frombuffer(message.value, np.uint8)
                frame = cv.imdecode(np_arr, cv.IMREAD_COLOR)
                if not frame_queue.full():
                    frame_queue.put(frame)
        except Exception as e:
            print(f"Error processing message: {e}")
            break

def process_frames():
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    c.execute("SELECT * FROM user_info WHERE firstname = ?", (name,))
                    user_data = c.fetchone()
                    if user_data:
                        user_id, firstname, lastname, phone, sex, emergency_contact, division, image_paths_str = user_data
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

                        if not any(u['firstname'] == firstname and u['lastname'] == lastname for u in recognized_users):
                            recognized_users.append(user)

                            # Save to JSON
                            with open(output_file, 'w') as f:
                                json.dump(recognized_users, f, indent=4)
                            print(f"Updated report saved to {output_file}")

                            # Index in Elasticsearch
                            es.index(index=index_name, body=user)
                            print(f"Data for {firstname} {lastname} indexed to Elasticsearch.")

                # Draw rectangle and label on the frame
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

recognized_users = []
output_file = "/home/ephi471/Desktop/facial_analysis/recognized_users_report.json"
threading.Timer(40, archive_and_reset_json_file).start()

# Start Kafka consumer and frame processing
consume_thread = threading.Thread(target=consume_frames)
process_thread = threading.Thread(target=process_frames)
consume_thread.start()
process_thread.start()

consume_thread.join()
process_thread.join()

cv.destroyAllWindows()
conn.close()
