
import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



# Database and models
database_path = os.path.join(os.path.dirname(__file__), '..', 'DataBase', 'user_database.db')
known_face_encodings = np.load(os.path.join(os.path.dirname(__file__), '..', 'Model', 'known_face_encodings.npy'))
known_face_names = np.load(os.path.join(os.path.dirname(__file__), '..', 'Model', 'known_face_names.npy'))






