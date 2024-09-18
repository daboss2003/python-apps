
import bcrypt
from cs50 import SQL
from flask import Flask,flash,redirect,render_template,request,session,render_template_string,send_from_directory,jsonify,url_for
from flask_session import Session
from flask_bcrypt import Bcrypt
from datetime import datetime
from wtforms import FileField, StringField
from helpers import login_required,check_user,apology,escape_special_characters
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)
app.config["SECRET_KEY"] = "90909090"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]  = "filesystem"
Session(app)
bcrypt = Bcrypt(app)


db = SQL("sqlite:///project.db")
class UploadForm(FlaskForm):
    name = StringField('Image Name')
    description = StringField('Image Description')
    image = FileField('Image File')

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registration", methods=["POST","GET"])
def registration():
    """Register new users"""
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        role = request.form.get("role")
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        if check_user(username):
            return apology("username already exist")
        else:
            new_user = db.execute(
               "INSERT INTO users(username,hash,email,role)VALUES(?,?,?,?)",username, password, email, role
            )
            session["user_id"] = new_user
            flash("Registration Successful")
            user_id = session["user_id"]
            role  = db.execute("SELECT role FROM users WHERE id=?",user_id)
            roles = role[0]["role"]
            if roles == "professional":
                return redirect("/upload")
            else:
                return render_template("search.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")

        # Ensure password was submitted
        password =  request.form.get("password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )
        
        

        # Ensure username exists and password is correct
        if len(rows) != 1 or not bcrypt.check_password_hash(
            rows[0]["hash"], password
        ):
            return apology(
                "invalid username and/or password"
            )
            

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        user_id = session["user_id"]
        role  = db.execute("SELECT role FROM users WHERE id=?",user_id)
        roles = role[0]["role"]
        confirm  = db.execute("SELECT is_confirmed FROM users WHERE id=?",user_id)
        is_confirmed = confirm[0]["is_confirmed"]
        if roles == "professional" and is_confirmed == 1:
            return redirect("/profile")
        elif roles == "professional" and is_confirmed == 0:
            return render_template("confirm.html")
        else:
            return render_template("search.html")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/upload',methods=["GET","POST"])
@login_required
def upload():
    form = UploadForm()
    """Upload user image for profile picture"""
    
    if request.method == 'POST' and form.validate_on_submit():
        user_id = session["user_id"]
        name = form.name.data
        description = form.description.data
        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            file_path = (os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image.save(file_path)
            db.execute("INSERT INTO image (image_name,image_description,filename,user_id) VALUES(?,?,?,?)",name,description,filename,user_id)
            flash("Image uploaded successfully!")
            return render_template("confirm.html")
        else:
            return render_template('upload.html',form=form, title='Upload')
            
    else:
        form = UploadForm()
        return render_template('upload.html',form=form, title='Upload')
        
@app.route('/confirm',methods=['POST','GET'])
@login_required
def confirm():
    """profile setup for professional after successful login"""
    if request.method == 'POST':
        user_id = session["user_id"]
        experience_count = int(request.form.get('experience_count',0))
        for i in range (experience_count):
            experience_date = request.form.get(f"experiencedate_{i}")
            experience_value = request.form.get(f"experience_{i}")
            db.execute("INSERT INTO user_experience(user_id,experience_date,experience_value) VALUES (?,?,?)",user_id,experience_date,experience_value)
            
        education_count = int(request.form.get('education_count',0))
        for i in range (education_count):
            education_date = request.form.get(f"educationdate_{i}")
            education_value = request.form.get(f"education_{i}")
            db.execute("INSERT INTO user_education(user_id,education_date,education_value) VALUES (?,?,?)",user_id,education_date,education_value)
        
        certificate_count = int(request.form.get('certificate_count',0))
        for i in range (certificate_count):
            certificate_date = request.form.get(f"certificationdate_{i}")
            certificate_value = request.form.get(f"certificate_{i}")
            db.execute("INSERT INTO user_certification(user_id,certification_date,certification_value) VALUES (?,?,?)",user_id,certificate_date,certificate_value)
        
        skill_count = int(request.form.get('skill_count',0))
        for i in range (skill_count):
            skills = request.form.get(f"skills_{i}")
            db.execute("INSERT INTO skills(user_id,skills) VALUES(?,?)",user_id,skills)
            
            
        fullname = request.form.get('fullname')
        status = request.form.get('Status')
        description = request.form.get('description')
        job = request.form.get('job')
        address = request.form.get('address')
        availability = request.form.get('availability')
        work_location = request.form.get('work_pattern')
        review = request.form.get('review')
        user_link = request.form.get('user_link')
        
        
        
        
        db.execute("INSERT INTO profiles (user_id,fullname,status,description,job,address,availability,work_location,review,user_link) VALUES(?,?,?,?,?,?,?,?,?,?)",user_id,fullname,status,description,job,address,availability,work_location,review,user_link)
        db.execute("UPDATE users SET is_confirmed=1")
        flash("Profile creation successful")
        return redirect("/profile")
    
    
    return render_template("confirm.html")
        
    
@app.route("/profile",methods=['GET','POST']) 
@login_required
def profile():
     """profile page"""
     if request.method == 'GET':
        user_id = session["user_id"]
        is_confirmed = db.execute("SELECT is_confirmed FROM users WHERE id=?",user_id)
        confirm = is_confirmed[0]["is_confirmed"]
        if confirm == 0:
            flash("Please set up your profile first")
            return redirect("/confirm")
        else:
            profiles = db.execute("SELECT fullname,status,description,job,address,availability,work_location,review,user_link FROM profiles WHERE user_id=?",user_id)
            
            fullname = profiles[0]["fullname"]
            status = profiles[0]["status"]
            description = profiles[0]["description"]
            job = profiles[0]["job"]
            address = profiles[0]["address"]
            availability = profiles[0]["availability"]
            work_location = profiles[0]["work_location"]
            review = profiles[0]["review"]
            user_link = profiles[0]["user_link"]
            
            
            
            usernames = db.execute("SELECT username FROM users WHERE id=?",user_id)
            username = usernames[0]["username"]
            times = db.execute("SELECT date FROM users WHERE id=?",user_id)
            timestampst = times[0]['date']
            timestamps = datetime.strptime(timestampst,'%Y-%m-%d %H:%M:%S')
            timestamp = int(timestamps.timestamp())
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            
            
            experience = db.execute("SELECT experience_date,experience_value FROM user_experience WHERE user_id=? ORDER BY experience_date DESC",user_id)
            education = db.execute("SELECT education_date,education_value FROM user_education WHERE user_id=? ORDER BY education_date DESC ",user_id)
            
            certification = db.execute("SELECT certification_date,certification_value FROM user_certification WHERE user_id=? ORDER BY certification_date DESC",user_id)
            
            
            skills = db.execute("SELECT skills FROM skills WHERE user_id=? ORDER BY skills DESC;",user_id)
            
            images = db.execute("SELECT filename FROM image WHERE user_id=?",user_id)
            image = images[0]["filename"]
            
            roles = db.execute("SELECT role FROM users WHERE id=?",user_id)
            role = roles[0]["role"]
            id = db.execute("SELECT sender_id FROM messages WHERE reciever_id=?",user_id)
            if not id:
                sender_id = 0
            else:
                sender_id = id[0]["sender_id"]
            return render_template("profile.html",profiles=profiles,username=username,experience=experience,education=education,certification=certification,skills=skills,image=image,date=date,fullname=fullname,status=status,description=description,job=job,address=address,availability=availability,work_location=work_location,review=review,user_link=user_link,role=role,sender_id=sender_id)
    

@app.route('/upload_file/<filename>')
def upload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



     
@app.route('/update',methods=['GET','POST'])
@login_required
def update() :
    if request.method == 'POST':
        user_id = session["user_id"]
        experience_count = int(request.form.get('experience_count',0))
        db.execute("DELETE FROM user_experience WHERE user_id =?",user_id)
        for i in range (experience_count):
            experience_date = request.form.get(f"experiencedate_{i}")
            experience_value = request.form.get(f"experience_{i}")
            db.execute("INSERT INTO user_experience(user_id,experience_date,experience_value) VALUES (?,?,?)",user_id,experience_date,experience_value)
            
        education_count = int(request.form.get('education_count',0))
        db.execute("DELETE FROM user_education WHERE user_id=?",user_id)
        for i in range (education_count):
            education_date = request.form.get(f"educationdate_{i}")
            education_value = request.form.get(f"education_{i}")
            db.execute("INSERT INTO user_education(user_id,education_date,education_value) VALUES (?,?,?)",user_id,education_date,education_value)
        
        certificate_count = int(request.form.get('certificate_count',0))
        db.execute("DELETE FROM user_certification WHERE user_id=?",user_id)
        for i in range (certificate_count):
            certificate_date = request.form.get(f"certificationdate_{i}")
            certificate_value = request.form.get(f"certificate_{i}")
            db.execute("INSERT INTO user_certification(user_id,certification_date,certification_value) VALUES (?,?,?)",user_id,certificate_date,certificate_value)
        
        skill_count = int(request.form.get('skill_count',0))
        db.execute("DELETE FROM skills WHERE user_id=?",user_id)
        for i in range (skill_count):
            skills = request.form.get(f"skills_{i}")
            db.execute("INSERT INTO skills(user_id,skills) VALUES(?,?)",user_id,skills)
            
            
        fullname = request.form.get('fullname')
        status = request.form.get('Status')
        description = request.form.get('description')
        job = request.form.get('job')
        address = request.form.get('address')
        availability = request.form.get('availability')
        work_location = request.form.get('work_pattern')
        review = request.form.get('review')
        user_link = request.form.get('user_link')
        
        
        db.execute("UPDATE profiles SET fullname =?,status =?,description =?,job =?,address =?,availability =?,work_location =?,review =?,user_link =? WHERE user_id=?",fullname,status,description,job,address,availability,work_location,review,user_link,user_id)
        flash("Profile Update successful")
        return redirect("/profile")
    
    
    return render_template("update.html")
        
    
@app.route("/delete",methods=["GET","POST"])  
@login_required
def delete() :
    if request.method == 'POST':
        selected_choice = request.form.get("selected_choice")
        if selected_choice == "Yes":
            user_id = session["user_id"]
            db.execute("DELETE FROM image WHERE user_id=?",user_id)
            db.execute("DELETE FROM profiles WHERE user_id=?",user_id)
            db.execute("DELETE FROM user_experience WHERE user_id=?",user_id)
            db.execute("DELETE FROM user_education WHERE user_id=?",user_id)
            db.execute("DELETE FROM user_certification WHERE user_id=?",user_id)
            db.execute("DELETE FROM skills WHERE user_id=?",user_id)
            db.execute("DELETE FROM users WHERE id=?",user_id)
            flash("Account deleted successfully")
            return redirect("/")
        else:
            return redirect("/profile")
    return render_template("delete.html")
        

@app.route("/back_to_search")
def back_to_search():
    return render_template("search.html")

@app.route("/search")
@login_required
def search_professionals():

    query = request.args.get('query','').lower()
    if not query:
        return jsonify([])
    try:
        results = db.execute("SELECT user_id,fullname,job,description FROM profiles WHERE LOWER(fullname) LIKE ? OR LOWER(job) LIKE ? OR LOWER(description) LIKE ? ",f"%{query}%",f"%{query}%",f"%{query}%")
        print(results)
        return jsonify(results)
    except Exception as e:
        print(f"Error during search:{e}")
        return jsonify({'error':'internal server error'}),500
            

@app.route("/profile_pics",methods=['GET','POST'])
@login_required
def profile_pics():
    form = UploadForm()
    """Upload user image for profile picture"""
    
    if request.method == 'POST' and form.validate_on_submit():
        user_id = session["user_id"]
        name = form.name.data
        description = form.description.data
        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            file_path = (os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image.save(file_path)
            db.execute("UPDATE image SET image_name =?,image_description=?,filename =? WHERE user_id =?",name,description,filename,user_id)
            flash("Image updated successfully!")
            return redirect("/profile")
        else:
            return render_template('profile_pics.html',form=form, title='Upload')
            
    else:
        form = UploadForm()
        return render_template('upload.html',form=form, title='Upload')
        

@app.route("/message/<int:reciever_id>",methods=['GET','POST'])
def message(reciever_id):
    if request.method == 'POST':
        sender_id = session["user_id"]
        message_content = request.form.get('message_content')
        db.execute("INSERT INTO messages (sender_id,reciever_id,content) VALUES(?,?,?)",sender_id,reciever_id,message_content)
        flash("Message sent Successfully!")
        messages = db.execute("SELECT * FROM messages WHERE (sender_id =? AND reciever_id = ?) OR (sender_id =? AND reciever_id = ?)ORDER BY timestamp",sender_id,reciever_id,reciever_id,sender_id)
        sender_name = db.execute("SELECT username FROM users WHERE id=?",sender_id)
        sender_name = sender_name[0]["username"]
        return render_template("messages.html",messages=messages,reciever_id=reciever_id,sender_name=sender_name)
    else:
        sender_id = session["user_id"]
        messages = db.execute("SELECT * FROM messages WHERE (sender_id =? AND reciever_id = ?) OR (sender_id =? AND reciever_id = ?)ORDER BY timestamp",sender_id,reciever_id,reciever_id,sender_id)
        if not messages:
            return render_template("messages.html",reciever_id=reciever_id)
        else:
            return render_template("messages.html",reciever_id=reciever_id,messages=messages)








@app.route("/view_profile/<int:id>",methods=['GET','POST'])
def view_profile(id):
    
    if request.method == 'GET':
        user_id = id
        
        profiles = db.execute("SELECT fullname,status,description,job,address,availability,work_location,review,user_link FROM profiles WHERE user_id=?",user_id)
        
        fullname = profiles[0]["fullname"]
        status = profiles[0]["status"]
        description = profiles[0]["description"]
        job = profiles[0]["job"]
        address = profiles[0]["address"]
        availability = profiles[0]["availability"]
        work_location = profiles[0]["work_location"]
        review = profiles[0]["review"]
        user_link = profiles[0]["user_link"]
        
        
        
        usernames = db.execute("SELECT username FROM users WHERE id=?",user_id)
        username = usernames[0]["username"]
        times = db.execute("SELECT date FROM users WHERE id=?",user_id)
        timestampst = times[0]['date']
        timestamps = datetime.strptime(timestampst,'%Y-%m-%d %H:%M:%S')
        timestamp = int(timestamps.timestamp())
        date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        
        
        experience = db.execute("SELECT experience_date,experience_value FROM user_experience WHERE user_id=? ORDER BY experience_date DESC",user_id)
        education = db.execute("SELECT education_date,education_value FROM user_education WHERE user_id=? ORDER BY education_date DESC ",user_id)
        
        certification = db.execute("SELECT certification_date,certification_value FROM user_certification WHERE user_id=? ORDER BY certification_date DESC",user_id)
        
        
        skills = db.execute("SELECT skills FROM skills WHERE user_id=? ORDER BY skills DESC;",user_id)
        
        images = db.execute("SELECT filename FROM image WHERE user_id=?",user_id)
        image = images[0]["filename"]
        
        roles = db.execute("SELECT role FROM users WHERE id=?",user_id)
        role = roles[0]["role"]
        
        return render_template("view_profile.html",profiles=profiles,username=username,experience=experience,education=education,certification=certification,skills=skills,image=image,date=date,fullname=fullname,status=status,description=description,job=job,address=address,availability=availability,work_location=work_location,review=review,user_link=user_link,role=role,user_id=user_id)


@app.route("/no_message")
def no_message():
    return render_template("no_message.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)