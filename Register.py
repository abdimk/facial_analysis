import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import cv2
from PIL import Image, ImageTk


faceCascade = cv2.CascadeClassifier('Assets/haarcascade_frontalface_default.xml')

conn = sqlite3.connect('DataBase/user_database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_info
             (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname text, lastname text, phone text, sex text, emergency_contact text, division text, image)''')
def update_camera_feed():
    global cap
    ret, img = cap.read()
    if ret:
        
        img = cv2.resize(img, (320, 240))
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)

       
        preview_label.config(image=imgtk)
        preview_label.image = imgtk  

    root.after(10, update_camera_feed)

def capture_image():
    global captured_images
    ret, frame = cap.read()
    if ret and len(captured_images) < 5:
        captured_images.append(frame)
        messagebox.showinfo("Capture", f"Captured image {len(captured_images)} of 5")

def save_user_info():
    if len(captured_images) < 5:
        messagebox.showwarning("Warning", "Please capture 5 images before saving.")
        return

    firstname = firstname_entry.get()
    lastname = lastname_entry.get()
    phone = phone_entry.get()
    sex = sex_combobox.get()
    emergency_contact = emergency_contact_entry.get()
    division = division_combobox.get()

    c.execute("INSERT INTO user_info (firstname, lastname, phone, sex, emergency_contact, division) VALUES (?, ?, ?, ?, ?, ?)", 
              (firstname, lastname, phone, sex, emergency_contact, division))
    conn.commit()
    user_id = c.lastrowid

    try:
        image_paths = []
        for i, frame in enumerate(captured_images):
            image_path = os.path.join('DataBase', 'userdb', f"{firstname}_{lastname}", f"{firstname}_{lastname}_{i+1}.jpg")
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            cv2.imwrite(image_path, frame)
            image_paths.append(image_path)
        
       
        image_paths_str = ','.join(image_paths)
        c.execute("UPDATE user_info SET image = ? WHERE id = ?", (image_paths_str, user_id))
        conn.commit()
        messagebox.showinfo("Success", f"Information saved for {firstname} {lastname}")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving information: {e}")

   
    clear_fields()

def clear_fields():
    global captured_images
    captured_images = []
    firstname_entry.delete(0, tk.END)
    lastname_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    sex_combobox.set('')
    emergency_contact_entry.delete(0, tk.END)
    division_combobox.set('')

root = tk.Tk()
root.title("User Information Registration")
root.geometry("450x650")

preview_frame = ttk.Frame(root)
preview_frame.pack(pady=20)
preview_label = ttk.Label(preview_frame)
preview_label.pack()

input_frame = ttk.Frame(root, padding=20)
input_frame.pack(fill="both", expand=True)

firstname_label = ttk.Label(input_frame, text="First Name:", font=("Arial", 14))
firstname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
firstname_entry = ttk.Entry(input_frame, font=("Arial", 14))
firstname_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

lastname_label = ttk.Label(input_frame, text="Last Name:", font=("Arial", 14))
lastname_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
lastname_entry = ttk.Entry(input_frame, font=("Arial", 14))
lastname_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

phone_label = ttk.Label(input_frame, text="Phone:", font=("Arial", 14))
phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
phone_entry = ttk.Entry(input_frame, font=("Arial", 14))
phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

sex_label = ttk.Label(input_frame, text="Sex:", font=("Arial", 14))
sex_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
sex_combobox = ttk.Combobox(input_frame, font=("Arial", 14))
sex_combobox['values'] = ("M", "F")
sex_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

emergency_contact_label = ttk.Label(input_frame, text="Emergency Contact:", font=("Arial", 14))
emergency_contact_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
emergency_contact_entry = ttk.Entry(input_frame, font=("Arial", 14))
emergency_contact_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

division_label = ttk.Label(input_frame, text="Division:", font=("Arial", 14))
division_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
division_combobox = ttk.Combobox(input_frame, font=("Arial", 14))
division_combobox['values'] = ("Data Analytics", "Emerging", "AI", "Communication","Data Science")
division_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

capture_button = ttk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack(pady=10)

save_button = ttk.Button(root, text="Save", command=save_user_info)
save_button.pack(pady=10)

cap = cv2.VideoCapture(0)
captured_images = []

update_camera_feed()

root.mainloop()

cap.release()
conn.close()
