import sqlite3
import json
import os


conn = sqlite3.connect('DataBase/user_database.db')
c = conn.cursor()


c.execute("SELECT * FROM user_info")
rows = c.fetchall()


data = []
for row in rows:
    user_id = row[0]
    firstname = row[1]
    lastname = row[2]
    phone = row[3]
    sex = row[4]
    emergency_contact = row[5]
    division = row[6]
    image_paths_str = row[7]

    
    image_paths = image_paths_str.split(',')

    
    image_path_list = []
    for i, image_path in enumerate(image_paths):
        image_path_list.append(os.path.join('DataBase', 'userdb', f"{firstname}_{lastname}", f"{firstname}_{lastname}_{i+1}.jpg"))

    data.append({
        "id": user_id,
        "firstname": firstname,
        "lastname": lastname,
        "phone": phone,
        "sex": sex,
        "emergency_contact": emergency_contact,
        "division": division,
        "image_paths": image_path_list[0]
    })

conn.close()


print(json.dumps(data))
