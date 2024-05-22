from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from io import BytesIO
import os
from telegram import Bot
from flask_mail import Mail, Message
import requests
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="wcDKxxCya6kJIpda6sK2"
)


app = Flask(__name__)

bot_token = '7109066009:AAF5dilbMQrgxd6fdHvRvOGPas-yBBLfvYQ'
CID = "1453432519"
msg = "Booking Succesfully Made!"
# app.config['SECRET_KEY'] = 'your_secret_key_here'
# app.config['MAIL_SERVER'] = 'eyedisease.local'  # Your SMTP server
# app.config['MAIL_PORT'] = 5000  # Port of your SMTP server
# app.config['MAIL_USE_TLS'] = True  # Enable TLSmailto:mainproject0404@gmail.com
# app.config['MAIL_USERNAME'] = 'mainproject0404@gmail.com'  # Your email username
# app.config['MAIL_PASSWORD'] = 'pROJECT!321'  # Your email password
# app.config['MAIL_DEFAULT_SENDER'] = 'mainproject0404@gmail.com'
username = ""
mail = Mail(app)


# SCOPES = [
#         "https://www.googleapis.com/auth/gmail.send"
#     ]
# flow = InstalledAppFlow.from_client_secrets_file('clientkey.json', SCOPES)
# creds = flow.run_local_server(port=0)




# Your credentials file path
credentials_file_path = 'servicekey.json'
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

# Create credentials object
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_file_path, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())




# def send_email(email, subject, message):
    # msg = MIMEMultipart('alternative')
    # # msg.set_content(message)
    # messag = MIMEText(message, 'plain')
    # msg.attach(messag)
    # msg['Subject'] = subject
    # msg['From'] = email  # Change this to your email
    # msg['To'] = 'sayanths@gmail.com'
    # sender_email = email
    # # password = 'your_password'

    # with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    #     smtp.starttls()
    #     smtp.login('mainproject0404@gmail.com', 'pROJECT!321')  # Change this to your email and password
    #     smtp.sendmail(sender_email, 'sayanths@gmail.com', msg.as_string())
    
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'admin' and password == '123456':
        return redirect(url_for('success'))
    else:
        error = 'Invalid username or password. Please try again.'
        return render_template('login.html', error=error)

@app.route('/success')
def success():
    return render_template('detectionPage.html')

@app.route('/result', methods=["POST"])
def result():
    model = tf.keras.models.load_model("./modelFile/eyeDisease.h5")
    CLASSES = [ 'Cataract', 'Diabetic Retinopathy', 'Glaucoma', 'Normal', 'Null' ]
    
    file = request.files['image']
    file_contents = file.read()
    filename = os.path.join('static', file.filename)
    with open('static/css/img/result.jpg', 'wb') as f:
        f.write(file_contents)
        
    # Set the confidence threshold (e.g., 70%)
    confidence_threshold = 70

    # Perform inference with the adjusted confidence threshold
    result = CLIENT.infer("static/css/img/result.jpg", model_id="eyedisease-1/1")

    # Process the result
    if 'predictions' in result:
        predictions = result['predictions']
        if predictions:
            max_confidence = 0
        max_confidence_prediction = None
        
        # Iterate over predictions to find the one with the highest confidence
        for prediction in predictions:
            class_name = prediction['class']
            confidence = prediction['confidence'] * 100
            
            # Check if current prediction has higher confidence than previous ones
            if confidence > max_confidence:
                max_confidence = confidence
                max_confidence_prediction = class_name
        
        if max_confidence_prediction:
            return render_template('detectionPage.html', result=max_confidence_prediction, confidence_level=max_confidence)

    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    predicted_class = np.argmax(preds)
    confidence_level = preds[0][predicted_class] * 100
    # print(preds[0])
    # print(predicted_class)
    result = CLASSES[predicted_class]
    return render_template('detectionPage.html', result=result, confidence_level=confidence_level) 

@app.route('/contact', methods=['POST'])
def cont():
    if request.method == 'POST':
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={CID}&text={msg}"
        print(requests.get(url).json())
        name = request.form['name']
        number = request.form['number']
        mail = request.form['email']
        doctor_mail = "arpitramesan777@gmail.com"
        subject = "Booking for appoinment!"
        messge = "I am writing to confirm my appointment for an eye examination at your esteemed clinic. My name is "+ name +", and you may reach me at " + number + " in case of any changes or queries. The purpose of my visit is a routine eye examination to ensure optimal eye health.\nI understand the importance of regular check-ups for maintaining good vision, and I am eager to discuss any concerns or questions I may have during the appointment. Please let me know if there are any specific preparations I need to make beforehand, or if there are any forms I should fill out prior to my visit.\nYour attention to this matter is greatly appreciated. If there are any changes to the appointment or if rescheduling becomes necessary, please do not hesitate to inform me as soon as possible.\nLooking forward to meeting with you soon.\nWarm Regards\n"+ username
        
        service = build('gmail', 'v1', credentials=creds)
        def create_message(sender, to, subject, message_text):
            message = {'raw': base64.urlsafe_b64encode(f"From: {sender}\nTo: {to}\nSubject: {subject}\n\n{message_text}".encode()).decode()}
            return message

        def send_message(service, user_id, message):
            try:
                message = (service.users().messages().send(userId=user_id, body=message).execute())
                print('Message Id: %s' % message['id'])
                return message
            except Exception as e:
                print('An error occurred: %s' % e)

        message = create_message(mail, doctor_mail, subject, messge)
        send_message(service, mail, message)
    return render_template('book.html')

if __name__ == '__main__':
    app.run(debug = True)