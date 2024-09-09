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

        self.faceCascade = cv2.CascadeClassifier('Assets/haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.cap.set(10, 60)
        self.captured_images = []

        self.message_shown = False
        # Create the database file if it doesn't exist
        self.database_path = r'DataBase/tuser_database.db'
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

        # Input fields
        labels = ["First Name:", "Last Name:", "Phone:", "Sex:", "Emergency Contact:", "Division:"]
        self.entries = []
        for i, label in enumerate(labels):
            ctk.CTkLabel(input_frame, text=label, font=("Arial", 14)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if label == "Sex:":
                entry = ctk.CTkComboBox(input_frame, values=["M", "F"], font=("Arial", 14))
            elif label == "Division:":
                entry = ctk.CTkComboBox(input_frame, values=["Data Analytics", "Emerging", "AI", "Communication", "Data Science"], font=("Arial", 14))
            else:
                entry = ctk.CTkEntry(input_frame, font=("Arial", 14))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries.append(entry)

        self.firstname_entry, self.lastname_entry, self.phone_entry, self.sex_combobox, self.emergency_contact_entry, self.division_combobox = self.entries

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
            ctk_img = ctk.CTkImage(light_image=img, size=(320, 240))

            self.preview_label.configure(image=ctk_img)
            self.preview_label.image = ctk_img
            self.preview_label.configure(text="")  # Set the text to an empty string to remove the label

        self.root.after(10, self.update_camera_feed)

    
    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            if len(self.captured_images) < 5:
                self.captured_images.append(frame)
                self.show_custom_message("Capture", f"Captured image {len(self.captured_images)} of 5")
            else:
                self.show_custom_message("Warning", "You have already captured 5 images.", "warning")

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
        if self.message_shown:
            return  # Prevent showing another message if one is already displayed

        self.message_shown = True  # Set the flag to true

        # Create a new top-level window for the message
        message_box = ctk.CTkToplevel(self.root)
        message_box.title(title)
        message_box.geometry("300x150")  # Set the window size (width x height)
        message_box.protocol("WM_DELETE_WINDOW", lambda: self.on_message_close(message_box))

        message_frame = ctk.CTkFrame(message_box)
        message_frame.pack(padx=20, pady=20, fill="both", expand=True)  # Fill the frame

        # Create a label for the message
        message_label = ctk.CTkLabel(message_frame, text=message, font=("Arial", 14), text_color="white")
        message_label.pack(pady=10, fill="both", expand=True)  # Make the label fill the frame

        # Create an OK button
        ok_button = ctk.CTkButton(message_frame, text="OK", command=lambda: self.on_message_close(message_box), fg_color="#333333", hover_color="#444444")
        ok_button.pack(pady=10)

        # Load the appropriate icon based on the message type
        if message_type == "info":
            icon = ctk.CTkImage(light_image=Image.open("Assets/info_icon.png"), size=(20, 20))
        elif message_type == "warning":
            icon = ctk.CTkImage(light_image=Image.open("Assets/warning_icon.png"), size=(20, 20))
        else:
            icon = ctk.CTkImage(light_image=Image.open("Assets/error_icon.png"), size=(20, 20))

        # Create a label for the icon
        icon_label = ctk.CTkLabel(message_frame, image=icon, text_color="white")
        icon_label.pack(side="left", padx=10)

        
    def on_message_close(self, message_box):
        self.message_shown = False  # Reset the flag when the message box is closed
        message_box.destroy()  # Destroy the message box

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
