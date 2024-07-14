import os
import pickle
import random
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def generate_otp():
    return random.randint(100000, 999999)


def create_mail(sender, to, subject, message_text):
    message = MIMEText(message_text) 
    message['to'] = to 
    message['from'] = sender 
    message['subject'] = subject 
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}


def send_mail(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute() 
        print(f"Message Id: {message['id']}")
        return message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

def main():

   

    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    

   
    otp = generate_otp()
    print(f"Generated OTP: {otp}")

    user_email = input("Enter your email address to receive an OTP: ")
    sender_email = "" 
    mail_body = f"Hello!\nYour OTP code is {otp}.\nPlease verify the OTP code."
    message = create_mail(sender_email, user_email, "Your OTP Code", mail_body)


    result = send_mail(service, "me", message) 
    if result:
        print("OTP sent successfully!")
    else:
        print("Failed to send OTP email.")
        quit()

    for i in range(1,4): 

        print(f"OTP verification {i}/3 triaL")
        try:
            user_otp = int(input("Enter the OTP you received: "))
        except ValueError:
            print("Invalid input. Please enter a numeric OTP.")
            continue

        if user_otp == otp:
            print("OTP verified successfully!")
            break
        else:
            print("Invalid OTP. Please try again.")
    else: 
        print("OTP not verified")

if __name__ == '__main__':
    main()