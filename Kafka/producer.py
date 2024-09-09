import signal
import sys
import subprocess
import cv2 as cv
from kafka import KafkaProducer, KafkaAdminClient
from kafka.errors import KafkaError



cap = None

def signal_handler(sig, frame):
    global cap
    print('\nStopping producer...')
    if cap is not None:
        cap.release()
    sys.exit(0)

def kafka_initialize(bootstrap_servers='localhost:9092'):
    global cap
    try:
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        print("Kafka is running on", bootstrap_servers)
        print("CTL-C to stop the producer")

        
        try:
            cap = cv.VideoCapture(0)
        except Exception as e:
            command =  "sudo kill -9 $(sudo fuser /dev/video0 2>&1 | awk '{print $NF}' | sed 's/m//')"
           
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return

        
        signal.signal(signal.SIGINT, signal_handler)  # Register Ctrl+C handler

        while True:
            ret, frame = cap.read()
            if not ret:
                break
           
            ret, buffer = cv.imencode('.jpg', frame)
            producer.send('video-stream', buffer.tobytes())

            if cv.waitKey(1) & 0xFF == ord('q'):
                print('The producer instance has stopped!')
                break
        
        producer.close()
        admin.close()
    except KafkaError as e:
        print(f"Kafka is not running: {e}")

    finally:
        if cap is not None:
            cap.release()

if __name__ == "__main__":
    kafka_initialize()
