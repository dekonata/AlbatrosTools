# Progam to generate faulty terminal email to HNA
# Must be run with with options in order: username, password, club name (full), replacement details
from asutils.webutils import AdminWebsite
from asutils.myfunctools import get_club_rounds
from asutils.teamworktools import get_max_ticket_id
from sys import argv
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path


# Uses clss in from webutils to log into admin website tor ecover number of members using username and password provided

admindriver = AdminWebsite(argv[1], argv[2], 'headless')

# Identify club and retrieve member count and club full name from admin.handicap website using AdminWebsite class get_club_playercoun method
club = input("Club: ")
club_details = admindriver.get_club_playercount(club)
members = club_details["Count"]
clubname = club_details["clubname"]

# Get number of rounds from rounds report CSV
rounds = get_club_rounds('./files/2021_Rounds_Report.csv', club)
ticket = (get_max_ticket_id(club))
ticketnr = str(ticket["ticket_id"])
ticket_date = ticket["created"]
ticket_subject = ticket["subject"]
faulty_model = input("Faulty Terminal Model: ")
replacement = input("Replacement Terminal Details: ")

print(
    f"""
Club Name:  {clubname}
Rounds:     {rounds}
Members:    {members}
ticketnr:   {ticketnr}
ticket_sub: {ticket_subject}
ticketdate: {ticket_date}
    """)

# Let user check if details retrieved are correct and stop running script if n is pressed
while True:
    check = input('Do you want to proceed sendint the email? y/n: ')
    if check == 'n':
        print('Please change arguments and try again')
        exit()
    elif check == 'y':
        break
    else:
        continue

# Substitute variables into html email template
html_email = Template(Path('./files/FaultyTermEmail.html').read_text())
substitute_dict = {
    'club': club,
    'members': members,
    'rounds': rounds,
    'replacement': replacement,
    'faulty_model': faulty_model
}

content = html_email.substitute(substitute_dict)
email = EmailMessage()
email['from'] = 'kriegler'
email['to'] = 'kriegler@albatrosgolf.co.za'
email['Subject'] = 'Ticket #' + ticketnr + ' | ' + club + ' | Faulty Terminal'
print(email.values())

email.set_content(content, 'html')

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()  # say hi open
    smtp.starttls()  # encrypt
    smtp.login('dekonata0@gmail.com', 'D8rp*49!')
    smtp.send_message(email)
    print('all good boss!')

