
import os
import numpy as np
import cv2 as cv
import face_recognition
from kafka import KafkaConsumer
import signal
import sys
import threading
from queue import Queue


known_face_encodings = np.load('known_face_encodings.npy')
known_face_names = np.load('known_face_names.npy')

frame_queue = Queue(maxsize=1)  # Limit the queue size to 10 frames
frame_processing_lock = threading.Lock()

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
                frame = cv.imdecode(np_arr, cv.IMREAD_COLOR)
                if not frame_queue.full():
                    frame_queue.put(frame)
        except Exception as e:
            print(f"Error processing message: {e}")
            break

def process_frames():
    while True:
        try:
            with frame_processing_lock:
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

                        
                        cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                       
                        label_text = name
                        label_size, _ = cv.getTextSize(label_text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)
                        label_width, label_height = label_size
                        label_x = left
                        label_y = top - 12 if top - 12 > 0 else top + 12
                        cv.rectangle(frame, (label_x - 2, label_y - 2), (label_x + label_width + 2, label_y + label_height + 2), (0, 255, 0), -1)
                        cv.putText(frame, label_text, (label_x, label_y + label_height), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                    
                    cv.imshow('Video', frame)

                    if cv.waitKey(1) & 0xFF == ord('q'):
                        print("Exit command received, shutting down...")
                        break
        except Exception as e:
            print(f"Error processing frame: {e}")

def main():
    
    signal.signal(signal.SIGINT, signal_handler)

    
    consume_thread = threading.Thread(target=consume_frames)
    process_thread = threading.Thread(target=process_frames)
    consume_thread.start()
    process_thread.start()

    
    consume_thread.join()
    process_thread.join()

        
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
