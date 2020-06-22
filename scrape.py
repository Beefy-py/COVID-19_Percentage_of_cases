"""
This program gets the percentage of people infected by the corona virus per country.
the percentage of active cases per country and the percentage of the total of people ever infected by country.
"""

'''
This program takes the data from a CoronaVirus website. https://www.worldometers.info/coronavirus/ and gives you the percentage of the population that has contracted coronavirus in total and the percentage of the population that currently has coronavirus by country.
'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = requests.get('https://www.worldometers.info/coronavirus/').text

soup = BeautifulSoup(url, 'lxml')

table = soup.find('table')
totalCases_and_activeCases_by_country_and_population = {}


def comma_str_value_to_int(value):
    if value == 'N/A':
        return None
    return int(''.join(value.split(',')))


for row in table.find_all('tr'):
    country_name = row.find('a')
    total_cases = row.find('td', style="font-weight: bold; text-align:right")
    active_cases = row.find('td', style="text-align:right;font-weight:bold;")
    population = row.find_all('td', style="font-weight: bold; text-align:right")

    if country_name is not None and total_cases is not None and active_cases is not None and population is not None:
        # converts total_cases, active_cases and population to integers
        total_cases = comma_str_value_to_int(total_cases.text)
        active_cases = comma_str_value_to_int(active_cases.text)
        population[-1] = comma_str_value_to_int(population[-1].text)
        totalCases_and_activeCases_by_country_and_population[country_name.text] = [total_cases,
                                                                                   active_cases,
                                                                                   population[-1]]

percent_active_per_country = []
percent_ever_tested_per_country = []


def get_current_percent():
    for country, act_cases in totalCases_and_activeCases_by_country_and_population.items():
        if act_cases[1] is None:
            pass
        else:
            print(
                f'({round(act_cases[1] / act_cases[2] * 100, 4)}%) of {country}\'s population has CoronaVirus per -- {datetime.today().strftime("%B %d %Y")}')


def get_all_time_percent():
    for country, tot_cases in totalCases_and_activeCases_by_country_and_population.items():
        if tot_cases[0] is None:
            pass
        else:
            print(
                f'The percentage of the total amount of people tested with CoronaVirus is ({round(tot_cases[0] / tot_cases[2] * 100, 4)}%) in {country} -- {datetime.today().strftime("%B %d %Y")}')


get_current_percent()
print()
get_all_time_percent()
