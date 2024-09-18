
import sqlite3
from flask import redirect, render_template, session
from functools import wraps
import re


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function








def check_user(username):
    connection = sqlite3.connect('project.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username =?",(username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result







conn = sqlite3.connect('project.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username TEXT NOT NULL,email TEXT NOT NULL,role TEXT NOT NULL, hash VARCHAR(300) NOT NULL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,is_confirmed BOOLEAN DEFAULT 0)")

cursor.execute("CREATE TABLE IF NOT EXISTS image(id INTEGER  PRIMARY KEY AUTOINCREMENT, image_name VARCHAR(250), image_description TEXT,filename VARCHAR(250),user_id INTEGER,FOREIGN KEY (user_id) REFERENCES users (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS profiles (id INTEGER  PRIMARY KEY AUTOINCREMENT, fullname TEXT NOT NULL, status TEXT NOT NULL,description TEXT NOT NULL,job TEXT NOT NULL, address TEXT NOT NULL, availability TEXT NOT NULL, work_location TEXT NOT NULL,review TEXT NOT NULL,user_link TEXT NOT NULL,user_id INTEGER,FOREIGN KEY (user_id) REFERENCES users (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS user_education (id INTEGER PRIMARY KEY AUTOINCREMENT,education_date TEXT NOT NULL,education_value TEXT NOT NULL,user_id INTEGER,FOREIGN KEY (user_id) REFERENCES users (id))")
conn.commit()
conn.close()



conn = sqlite3.connect('project.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_experience (id INTEGER  PRIMARY KEY AUTOINCREMENT,experience_date TEXT NOT NULL,experience_value TEXT NOT NULL,user_id INTEGER,FOREIGN KEY (user_id) REFERENCES users (id))")
cursor.execute("CREATE TABLE IF NOT EXISTS messages (sender_id INTEGER,reciever_id INTEGER, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (sender_id) REFERENCES users (id), FOREIGN KEY (reciever_id)REFERENCES users (id))")
conn.commit()
conn.close()



conn = sqlite3.connect('project.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_certification (id INTEGER  PRIMARY KEY AUTOINCREMENT, certification_date TEXT NOT NULL,certification_value TEXT NOT NULL,user_id INTEGER,FOREIGN KEY (user_id) REFERENCES users (id))")
conn.commit()
conn.close()


conn = sqlite3.connect('project.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS skills(id INTEGER PRIMARY KEY AUTOINCREMENT,skills,user_id INTEGER,FOREIGN KEY (user_id) REFERENCES users (id))")
conn.commit()
conn.close()


def escape_special_characters(input,replacement=' '):
    special_chars = re.compile(r'[&$#+\-()/;\'"*\|{}[\]^<>`~\\]')
    escaped_string = re.sub(special_chars,replacement,input)
    return escaped_string




