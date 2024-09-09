import numpy as np
import cv2 as cv
from kafka import KafkaConsumer
import signal
import sys

def signal_handler(sig, frame):
    print("Signal received, shutting down...")
    cv.destroyAllWindows()
    sys.exit(0)

def main():
    consumer = None
    try:
        # Register signal handler for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)

        # Initialize Kafka consumer
        consumer = KafkaConsumer('video-stream', bootstrap_servers='localhost:9092')

        while True:
            try:
                for message in consumer:
                    
                    np_arr = np.frombuffer(message.value, np.uint8)
                    frame = cv.imdecode(np_arr, cv.IMREAD_COLOR)

                    
                    cv.imshow('Video', frame)

                    if cv.waitKey(1) & 0xFF == ord('q'):
                        print("Exit command received, shutting down...")
                        break

            except Exception as e:
                print(f"Error processing message: {e}")
                break

    except Exception as e:
        print(f"Error initializing Kafka consumer: {e}")
    
    finally:
        if consumer:
            consumer.close()
        cv.destroyAllWindows()

if __name__ == "__main__":
    main()
