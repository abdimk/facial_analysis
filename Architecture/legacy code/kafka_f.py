import os
import numpy as np
import cv2 as cv
import face_recognition
from kafka import KafkaConsumer
import signal
import sys
import threading
from queue import Queue
import sqlite3

# Load the known face encodings and names from the saved files
known_face_encodings = np.load('known_face_encodings.npy')
known_face_names = np.load('known_face_names.npy')

# Database path
database_path = os.path.expanduser("/home/ephi471/Desktop/facial_analysis/DataBase/user_database.db")

frame_queue = Queue()

def signal_handler(sig, frame):
    print("Signal received, shutting down...")
    cv.destroyAllWindows()
    sys.exit(0)

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
                frame_queue.put(cv.imdecode(np_arr, cv.IMREAD_COLOR))
        except Exception as e:
            print(f"Error processing message: {e}")
            break

def process_frames():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    while True:
        try:
            frame = frame_queue.get()

            # Perform face recognition
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
                        print(f"Recognized: {firstname} {lastname}")
                        print(f"Phone: {phone}")
                        print(f"Sex: {sex}")
                        print(f"Emergency Contact: {emergency_contact}")
                        print(f"Division: {division}")

            # Optionally, you can add a delay or condition to avoid overwhelming the consumer
            # cv.imshow('Video', frame)  # Commented out to hide the video display

            if cv.waitKey(1) & 0xFF == ord('q'):
                print("Exit command received, shutting down...")
                break
        except Exception as e:
            print(f"Error processing frame: {e}")

    conn.close()

def main():
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Start the consume and process threads
    consume_thread = threading.Thread(target=consume_frames)
    process_thread = threading.Thread(target=process_frames)
    consume_thread.start()
    process_thread.start()

    # Wait for the threads to finish
    consume_thread.join()
    process_thread.join()

    # Clean up
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
