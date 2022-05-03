from bs4 import BeautifulSoup  # for scrapping the information
import requests  # for sending requests and getting html
from random import random
from time import sleep


url = "https://stackoverflow.com/questions"
questions = []
cur_page = 1
pages = 5

user_request = "json"

while cur_page <= pages:
    url = "https://stackoverflow.com/questions" + "?tab=votes" + "&page=" + str(cur_page)
    response = requests.get(url)  # getting request from the site with the html
    html = BeautifulSoup(response.text, 'html.parser')
    question_data = html.find_all('div', class_="s-post-summary js-post-summary")
    if question_data:
        questions.extend(question_data)
        some_ms = random()
        sleep(some_ms)
    else:
        print("No questions on English Stack Overflow")
        break
    cur_page += 1


score = []
href = []

for item in questions:
    if item.find('a', {"class": "s-link"}).text.lower().find(user_request.lower()) != -1:  # If the title suits the request
        if not (item.find('div', {"class": "s-post-summary--stats-item has-answers has-accepted-answer"}) is None):  # If there is a good answer
            score.append(int(item.find('span', {"class": "s-post-summary--stats-item-number"}).text))
            href.append("https://stackoverflow.com" + item.a.get('href'))


print(f"Hits found on English Stack Overflow: {len(score)}")
num_of_results = 5
i = 0
while i < min(num_of_results, len(score) + i):
    print(f"Votes: {score[score.index(max(score), 0)]} ---->\t{href[score.index(max(score), 0)]}")
    href.pop(score.index(max(score), 0))
    score.pop(score.index(max(score), 0))
    i += 1


questions = []
cur_page = 1


while cur_page <= pages:
    url = "https://ru.stackoverflow.com/questions" + "?tab=votes" + "&page=" + str(cur_page)
    response = requests.get(url)  # getting request from the site with the html
    html = BeautifulSoup(response.text, 'html.parser')
    question_data = html.find_all('div', class_="s-post-summary js-post-summary")
    if question_data:
        questions.extend(question_data)
        some_ms = random()
        sleep(some_ms)
    else:
        print("No questions on Russian Stack Overflow")
        break
    cur_page += 1


score = []
href = []

for item in questions:
    if item.find('a', {"class": "s-link"}).text.lower().find(user_request.lower()) != -1:  # If the title suits the request
        if not (item.find('div', {"class": "s-post-summary--stats-item has-answers has-accepted-answer"}) is None):  # If there is a good answer
            score.append(int(item.find('span', {"class": "s-post-summary--stats-item-number"}).text))
            href.append("https://ru.stackoverflow.com" + item.a.get('href'))


# This part of code finds ALL of most voted answers
# start = 0
# try:
#     while True:
#         i = score.index(max(score), start)
#         print(score[i], href[i], sep='\t')
#         answer_url = href[i]
#         answer_response = requests.get(answer_url)
#         answer_html = BeautifulSoup(answer_response.text, 'html.parser')
#         start = score.index(max(score), start + 1)
# except ValueError:
#     pass


print(f"Hits found on Russian Stack Overflow: {len(score)}")
num_of_results = 5
i = 0
while i < min(num_of_results, len(score) + i):
    print(f"Votes: {score[score.index(max(score), 0)]} ---->\t{href[score.index(max(score), 0)]}")
    href.pop(score.index(max(score), 0))
    score.pop(score.index(max(score), 0))
    i += 1


