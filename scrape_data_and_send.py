"""
This script gets the percentage of people infected by the corona virus per country.
the percentage of active cases per country and the percentage of the total of people ever infected by country.
"""

import requests
import smtplib, ssl, os
from bs4 import BeautifulSoup
from datetime import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

url = requests.get('https://www.worldometers.info/coronavirus/').text

soup = BeautifulSoup(url, 'html.parser')

table = soup.find('table')


def comma_str_value_to_int(value):
    if value == 'N/A':
        return None
    return int(''.join(value.split(',')))


percentage_total_cases = []
percentage_active_cases = []
total_cases_out = []
active_cases_out = []
populations = []
countries = []

ALL_DATA={}

for row in table.find_all('tr'):
    country_name = row.find('a')
    total_cases = row.find('td', style="font-weight: bold; text-align:right")
    active_cases = row.find('td', style="text-align:right;font-weight:bold;")
    population = row.find_all('td', style="font-weight: bold; text-align:right")

    if country_name is not None and total_cases is not None and active_cases is not None and population is not None:
        total_cases_out.append(comma_str_value_to_int(total_cases.text))
        active_cases_out.append(comma_str_value_to_int(active_cases.text))
        populations.append(comma_str_value_to_int(population[-1].text))
        countries.append(country_name)


def to_percentages(parts, wholes):
    output = []
    for i, e in zip(parts, wholes):
        if i is None or e is None:
            output.append('Not Calculated')
        else:
            output.append(f'{round((i / e) * 100, 4)}%')
    return output


percentage_active_cases = to_percentages(active_cases_out, populations)
percentage_total_cases = to_percentages(total_cases_out, populations)


sender_email = os.environ['SENDER_EMAIL']
sender_password = os.environ['SENDER_PASSWORD']

receiver_email = 'hoftkenny@gmail.com'

message = MIMEMultipart('alternative')
message['Subject'] = 'CoronaVirus Data'
message['From'] = sender_email
message['To'] = receiver_email

# plain text msg
plain_text = """\
Hi there. This data is currently unavailable in plain text format"""

# html msg
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('message.html')
html = template.render(message_body=message,
                       percentage_active_cases=percentage_active_cases,
                       percentage_total_cases=percentage_total_cases,
                       total_cases_out=total_cases_out,
                       active_cases_out=active_cases_out,
                       countries=countries,
                       populations=populations
                       )

text_version = MIMEText(plain_text, 'plain')
html_version = MIMEText(html, 'html')

message.attach(text_version)
message.attach(html_version)

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=context) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
