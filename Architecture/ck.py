import customtkinter as ctk
from PIL import ImageTk, Image
import sqlite3
import os
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox

class UserRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Information Registration")
        self.root.geometry("400x640")

        self.faceCascade = cv2.CascadeClassifier('/home/ephi471/Desktop/facial_analysis/Assets/haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.captured_images = []

        # Create the database file if it doesn't exist
        self.database_path = r'DataBase/user_database.db'
        if not os.path.exists(os.path.dirname(self.database_path)):
            os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
        self.conn = sqlite3.connect(self.database_path)
        self.c = self.conn.cursor()

        # Create the user_info table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS user_info
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname text, lastname text, phone text, sex text, emergency_contact text, division text, image)''')
        self.conn.commit()

        self.create_gui()
        self.update_camera_feed()

    def create_gui(self):
        self.preview_frame = ctk.CTkFrame(self.root)
        self.preview_frame.pack(pady=20)
        self.preview_label = ctk.CTkLabel(self.preview_frame)
        self.preview_label.pack()

        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(fill="both", expand=True, padx=20, pady=20)

        firstname_label = ctk.CTkLabel(input_frame, text="First Name:", font=("Arial", 14))
        firstname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.firstname_entry = ctk.CTkEntry(input_frame, font=("Arial", 14))
        self.firstname_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        lastname_label = ctk.CTkLabel(input_frame, text="Last Name:", font=("Arial", 14))
        lastname_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.lastname_entry = ctk.CTkEntry(input_frame, font=("Arial", 14))
        self.lastname_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        phone_label = ctk.CTkLabel(input_frame, text="Phone:", font=("Arial", 14))
        phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = ctk.CTkEntry(input_frame, font=("Arial", 14))
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        sex_label = ctk.CTkLabel(input_frame, text="Sex:", font=("Arial", 14))
        sex_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.sex_combobox = ctk.CTkComboBox(input_frame, values=["M", "F"], font=("Arial", 14))
        self.sex_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        emergency_contact_label = ctk.CTkLabel(input_frame, text="Emergency Contact:", font=("Arial", 14))
        emergency_contact_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.emergency_contact_entry = ctk.CTkEntry(input_frame, font=("Arial", 14))
        self.emergency_contact_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        division_label = ctk.CTkLabel(input_frame, text="Division:", font=("Arial", 14))
        division_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.division_combobox = ctk.CTkComboBox(input_frame, values=["Data Analytics", "Emerging", "AI", "Communication", "Data Science"], font=("Arial", 14))
        self.division_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.capture_button = ctk.CTkButton(self.root, text="Capture Image", command=self.capture_image)
        self.capture_button.pack(pady=10)

        self.save_button = ctk.CTkButton(self.root, text="Save", command=self.save_user_info)
        self.save_button.pack(pady=10)


    def update_camera_feed(self):
        ret, img = self.cap.read()
        if ret:
            img = cv2.resize(img, (320, 240))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

            # Convert the PIL image to CTkImage
            ctk_img = ctk.CTkImage(light_image=img, size=(320, 240))

            self.preview_label.configure(image=ctk_img)
            self.preview_label.image = ctk_img

        self.root.after(10, self.update_camera_feed)




    def capture_image(self):
        ret, frame = self.cap.read()
        if ret and len(self.captured_images) < 5:
            self.captured_images.append(frame)
            self.show_custom_message("Capture", f"Captured image {len(self.captured_images)} of 5")

    def save_user_info(self):
        if len(self.captured_images) < 5:
            self.show_custom_message("Warning", "Please capture 5 images before saving.", "warning")
            return

        # Rest of the save_user_info function cod


        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        phone = self.phone_entry.get()
        sex = self.sex_combobox.get()
        emergency_contact = self.emergency_contact_entry.get()
        division = self.division_combobox.get()

        try:
            self.c.execute("INSERT INTO user_info (firstname, lastname, phone, sex, emergency_contact, division) VALUES (?, ?, ?, ?, ?, ?)", 
                        (firstname, lastname, phone, sex, emergency_contact, division))
            self.conn.commit()
            user_id = self.c.lastrowid

            image_paths = []
            for i, frame in enumerate(self.captured_images):
                image_path = os.path.join('DataBase', 'userdb', f"{firstname}_{lastname}", f"{firstname}_{lastname}_{i+1}.jpg")
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                cv2.imwrite(image_path, frame)
                image_paths.append(image_path)
            
            image_paths_str = ','.join(image_paths)
            self.c.execute("UPDATE user_info SET image = ? WHERE id = ?", (image_paths_str, user_id))
            self.conn.commit()
            messagebox.showinfo("Success", f"Information saved for {firstname} {lastname}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving information: {e}")
        finally:
            self.conn.close()

        self.clear_fields()

    def show_custom_message(self, title, message, message_type="info"):
        if message_type == "info":
            icon = ctk.CTkImage(light_image=Image.open("Assets/info_icon.png"), size=(20, 20))
        elif message_type == "warning":
            icon = ctk.CTkImage(light_image=Image.open("Assets/warning_icon.png"), size=(20, 20))
        else:
            icon = ctk.CTkImage(light_image=Image.open("Assets/error_icon.png"), size=(20, 20))

        ctk.CTkToplevel(self.root).title(title)
        message_box = ctk.CTkFrame(ctk.CTkToplevel(self.root))
        message_box.pack(padx=20, pady=20)

        ctk.CTkLabel(message_box, text=message, font=("Arial", 14), text_color="white").pack(pady=10)
        ctk.CTkButton(message_box, text="OK", command=message_box.destroy, fg_color="#333333", hover_color="#444444").pack(pady=10)
        ctk.CTkLabel(message_box, image=icon, text_color="white").pack(side="left", padx=10)

    
    def clear_fields(self):
        self.captured_images = []
        self.firstname_entry.delete(0, ctk.END)
        self.lastname_entry.delete(0, ctk.END)
        self.phone_entry.delete(0, ctk.END)
        self.sex_combobox.set('')
        self.emergency_contact_entry.delete(0, ctk.END)
        self.division_combobox.set('')


    def __del__(self):
        self.cap.release()
        self.conn.close()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = ctk.CTk()
    app = UserRegistrationApp(root)
    root.mainloop()