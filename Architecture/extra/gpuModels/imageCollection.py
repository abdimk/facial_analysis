import cv2
import os
import time
import uuid
import subprocess

# Define labels and number of images to collect
labels = ['thumbsup',]
number_imgs = 5

# Setup folders for collected images
IMAGES_PATH = os.path.join('Tensorflow', 'workspace', 'images', 'collectedimages')
if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH)

for label in labels:
    path = os.path.join(IMAGES_PATH, label)
    if not os.path.exists(path):
        os.makedirs(path)

# Capture images for each label
for label in labels:
    cap = cv2.VideoCapture(0)
    print('Collecting images for {}'.format(label))
    time.sleep(5)  # Delay to position hands
    for imgnum in range(number_imgs):
        print('Collecting image {}'.format(imgnum))
        ret, frame = cap.read()
        imgname = os.path.join(IMAGES_PATH, label, f'{label}.{str(uuid.uuid1())}.jpg')
        cv2.imwrite(imgname, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)  # Delay between captures

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Install required packages for labeling
subprocess.run(['pip', 'install', '--upgrade', 'pyqt5', 'lxml'])

# Setup labelImg if not already cloned
LABELIMG_PATH = os.path.join('Tensorflow', 'labelimg')
if not os.path.exists(LABELIMG_PATH):
    os.makedirs(LABELIMG_PATH)
    subprocess.run(['git', 'clone', 'https://github.com/tzutalin/labelImg', LABELIMG_PATH])

# Launch labelImg for labeling images
if os.name == 'posix':
    subprocess.run(['make', 'qt5py3'], cwd=LABELIMG_PATH)
elif os.name == 'nt':
    subprocess.run(['pyrcc5', '-o', 'libs/resources.py', 'resources.qrc'], cwd=LABELIMG_PATH)

subprocess.run(['python', 'labelImg.py'], cwd=LABELIMG_PATH)

# Optional: Compress images for training
TRAIN_PATH = os.path.join('Tensorflow', 'workspace', 'images', 'train')
TEST_PATH = os.path.join('Tensorflow', 'workspace', 'images', 'test')
ARCHIVE_PATH = os.path.join('Tensorflow', 'workspace', 'images', 'archive.tar.gz')
subprocess.run(['tar', '-czf', ARCHIVE_PATH, TRAIN_PATH, TEST_PATH])

print("All steps completed.")
