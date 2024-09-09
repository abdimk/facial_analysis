import os
import numpy as np
import cv2 as cv
import face_recognition
import signal
import sys


encoding_dir = r"/Model/cpuModels"

known_face_encodings = np.load(os.path.join(encoding_dir, 'known_face_encodings.npy'))
known_face_names = np.load(os.path.join(encoding_dir, 'known_face_names.npy'))

def signal_handler(sig, frame):
    print("Signal received, shutting down...")
    cv.destroyAllWindows()
    sys.exit(0)

def main():
    
    signal.signal(signal.SIGINT, signal_handler)

   
    cap = cv.VideoCapture(0)

    while True:
        try:
           
            ret, frame = cap.read()

            # Perform face recognition
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Draw the rectangle around the face
                cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Draw the label with a nice format
                label_text = name
                label_size, _ = cv.getTextSize(label_text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)
                label_width, label_height = label_size
                label_x = left
                label_y = top - 12 if top - 12 > 0 else top + 12
                cv.rectangle(frame, (label_x - 2, label_y - 2), (label_x + label_width + 2, label_y + label_height + 2), (0, 255, 0), -1)
                cv.putText(frame, label_text, (label_x, label_y + label_height), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Display the frame
            cv.imshow('Video', frame)

            # Exit the loop if the 'q' key is pressed
            if cv.waitKey(1) & 0xFF == ord('q'):
                print("Exit command received, shutting down...")
                break
        except Exception as e:
            print(f"Error processing frame: {e}")

    # Release the camera and close all windows
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
