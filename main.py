from send_email import *
from fetch_details import *
import sqlite3
import schedule

###### Configuration ######

DB_PATH = "/Users/abm17/Desktop/Innovacer/Innovaccer/database.db"

EMAIL_TEMPLATE = '''Tv series name: _show_name_
Status: _status_
\n\n
'''
EMAIL_TIME = "10:30"

###### End of Configuration ######



# Function to update users in DB
def addUserDetailsToDB(user_details):
	try:
		conn = sqlite3.connect(DB_PATH)
		cur = conn.cursor()
	except Exception as excp:
		print "Error in connecting to DB. Please make sure the DB_Path is valid."

	for user_detail in user_details:
		try:
			cur.execute("""INSERT INTO users(email_id) VALUES("%s")"""%(user_detail["email"]))
			conn.commit()
		except Exception as excp:
			pass

		for show in user_detail["shows"]:
			try:
				cur.execute("""INSERT INTO shows(show_name,status) VALUES("%s","NA")"""%(show))
				conn.commit()
			except Exception as excp:
				pass

			try:
				cur.execute("""INSERT INTO user_preference(email_id,show_name) VALUES("%s","%s")"""%(user_detail["email"],show))
				conn.commit()
			except Exception as excp:
				pass

	print "Updated DB Successfully"
	return


# Fetches show status from IMDB and updates DB
def updateShowStatuses():
	try:
		conn = sqlite3.connect(DB_PATH)
		cur = conn.cursor()
	except Exception as excp:
		print "Error in connecting to DB. Please make sure the DB_Path is valid."
		return

	cur.execute("SELECT show_name from shows;")
	rows = cur.fetchall()
	show_list = [str(row[0]) for row in rows]
	
	for show in show_list:
		updated_status = getShowStatus(show)
		cur.execute("""UPDATE shows set status = "%s" where show_name="%s";""" %(updated_status,show))
		conn.commit()

	print "Updated Show Statuses"
	return


# Function to update DB
def parseInput():
	num_users = int(raw_input("Enter number of users to add: "))
	user_details = []
	for i in range(num_users):
		email_recipient = raw_input("Email Address: ")
		print "TV Series: "
		input_string = raw_input()
		input_string = input_string.lower()
		entries_list = input_string.split(',')
		entries_list = [entry.strip() for entry in entries_list]
		user_detail = {
		'email':email_recipient,
		'shows':entries_list
		}
		user_details.append(user_detail)
	return user_details

# Construcuts email list to be sent out to users
def constructEmails():
	emails_list = []
	try:
		conn = sqlite3.connect(DB_PATH)
		cur = conn.cursor()
	except Exception as excp:
		print "Error in connecting to DB. Please make sure the DB_Path is valid."
		return
	cur.execute("SELECT email_id from users;")
	rows = cur.fetchall()
	users_list = [str(row[0]) for row in rows]
	for user in users_list:
		email_dict = {}
		email_dict["email_id"] = user
		email_dict["email_body"] = ""
		cur.execute("""SELECT show_name from user_preference where email_id="%s";""" %(user))
		rows = cur.fetchall()
		shows_list = [str(row[0]) for row in rows]
		for show in shows_list:
			cur.execute("""SELECT status from shows where show_name="%s";""" %(show))
			rows = cur.fetchall()
			show_status = str(rows[0][0])
			show_reminder = EMAIL_TEMPLATE
			show_reminder = show_reminder.replace("_status_", show_status)
			show_reminder = show_reminder.replace("_show_name_", show.title())
			email_dict["email_body"] += show_reminder

		emails_list.append(email_dict)
	return emails_list		




# Sends out email reminders to users
def sendReminders():
	updateShowStatuses()
	emails_list = constructEmails()
	for email in emails_list:
		sendEmailReminder(email["email_id"],email["email_body"])


# Main function to control flow
def mainController():
	operation_mode = int(raw_input("Enter 1 to configure the script first or enter 2 to run the reminder service: "))
	if operation_mode == 1:
		user_details = parseInput()
		addUserDetailsToDB(user_details)

	schedule.every(1).minutes.do(sendReminders)
	while True:
		schedule.run_pending()
	


mainController()

