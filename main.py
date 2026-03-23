import os
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

load_dotenv()
app_email = os.getenv("APP_EMAIL")
app_pass = os.getenv("APP_PASS")

print(app_email)
print(app_pass)

app.config['SECRET_KEY'] = 'myapplication123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = app_email
app.config["MAIL_PASSWORD"] = app_pass

db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(100))

@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        available_start_date  = request.form['date']
        date_obj = datetime.strptime(available_start_date, '%Y-%m-%d')
        occupation = request.form['occupation']

        form = Form(first_name=first_name, last_name=last_name, email=email,
                    date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = (f"Thank you for your submission, {first_name}. \n"
                        f"Here is your data:\n{first_name} {last_name}"
                        f"\n{available_start_date} \n{occupation}\n"
                        f"Thank you!")
        message = Message(f"New form submission - {first_name} {last_name}",
                          sender='app_email',
                          recipients=[app_email],
                          body=message_body)
        mail.send(message)

        flash("Your form was submitted successfully!", "success")

    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)