import httplib2  
import os  
from httplib2 import Http  
from apiclient import discovery  
from apiclient import errors  
from time import sleep   
import oauth2client  
from oauth2client import client  
from oauth2client import tools  
   
import base64  
from email.mime.audio import MIMEAudio  
from email.mime.base import MIMEBase  
from email.mime.image import MIMEImage  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
import mimetypes  
   
try:  
  import argparse  
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()  
except ImportError:  
  flags = None  
   
SCOPES = 'https://mail.google.com/'  
CLIENT_SECRET_FILE = 'credentials.json'  
APPLICATION_NAME = 'Innovacer Project'  
   
   
def SendMessage(service, user_id, message):  
	try:
		message = (service.users().messages().send(userId=user_id, body=message).execute())  
		# print "Message Id: %s" % (message['id'])
		return message  
	except errors.HttpError, error:  
		print 'An error occurred: %s' % error 
   
   
def CreateMessage(sender, to, subject, message_text):  
	message = MIMEText(message_text)  
	message['to'] = to  
	message['from'] = sender  
	message['subject'] = subject  
	return {'raw': base64.b64encode(message.as_string())}  
   
def get_credentials():  
	home_dir = "./"
	credential_dir = os.path.join(home_dir, '.credentials')  
	if not os.path.exists(credential_dir):  
		os.makedirs(credential_dir)  
	credential_path = os.path.join(credential_dir, 'gmail-python-gmail.json')  
   
	store = oauth2client.file.Storage(credential_path)  
	credentials = store.get()  
	if not credentials or credentials.invalid:  
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)  
		flow.user_agent = APPLICATION_NAME  
		if flags:  
			credentials = tools.run_flow(flow, store, flags)  
		else: 
			credentials = tools.run(flow, store)  
		print 'Storing credentials to ' + credential_path
	return credentials  
   



def sendEmailReminder(reciever_email,email_body):
	credentials = get_credentials()  
	http = credentials.authorize(httplib2.Http())  
	service = discovery.build('gmail', 'v1', http=http)  
	subject = "TV Show Reminders"
	email_to = reciever_email
	email_body_message = email_body
	msg = CreateMessage('hypernova0610@gmail.com', email_to, subject, email_body_message)
	SendMessage(service, 'me', msg)
	sleep(1)


