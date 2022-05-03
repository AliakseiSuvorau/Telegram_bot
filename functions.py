from bs4 import BeautifulSoup  # for scrapping the information
import Globals as g
from random import random
import requests  # for sending requests and getting html
from time import sleep


def make_a_request_for_questions(base_url, score, href):
    """
    This function makes a list of answers, which are put into score ans href lists
    Arguments:
        base_url: the url of the head page of the site
        score: the list with numbers of votes for different answers
        href: the list of hyperlinks to the pages with answers
    Returns:
        Nothing
    """
    cur_page = 1
    while cur_page <= g.pages:
        questions = []
        url = base_url + str(cur_page)
        response = requests.get(url)  # getting request from the site with the html
        html = BeautifulSoup(response.text, 'html.parser')
        question_data = html.find_all('div', class_="s-post-summary js-post-summary")
        if question_data:
            questions.extend(question_data)
            some_ms = random()
            sleep(some_ms)
        else:
            break
        cur_page += 1
        look_for_answers(questions, score, href)
        if len(score) >= 5:
            break


def look_for_answers(questions, score, href):
    """
    This function looks for answers in found div containers
    Arguments:
        questions: the list with questions, which can potentially be the ones we're looking for
        score: the list with numbers of votes for different answers
        href: the list of hyperlinks to the pages with answers
    Returns:
        Nothing
    """
    for item in questions:
        if len(score) < g.num_of_results:
            # If the title suits the request
            if item.find('a', {"class": "s-link"}).text.lower().find(g.user_request.lower()) != -1:
                # If there is a good answer
                if not (item.find('div', {"class": "s-post-summary--stats-item has-answers has-accepted-answer"}) is None):
                    score.append(int(item.find('span', {"class": "s-post-summary--stats-item-number"}).text))
                    href.append("https://stackoverflow.com" + item.a.get('href'))
        else:
            break


def make_an_output(score, href):
    """
    This function makes a string of output, which is later to be sent to the user in telegram
    Arguments:
        score: the list with numbers of votes for different answers
        href: the list of hyperlinks to the pages with answers
    Returns:
        String with a part of an answer
    """
    answer_text = ""
    if len(score):
        if g.lan == "English":
            answer_text += "Most relevant hits found on English Stack Overflow:\n"
        else:
            answer_text += "Most relevant hits found on Russian Stack Overflow:\n"
    else:
        if g.lan == "English":
            return f"No answers found on English Stack Overflow on first {g.pages} pages\n"
        else:
            return f"No answers found on Russian Stack Overflow on first {g.pages} pages\n"
    i = 0
    while i < min(g.num_of_results, len(score) + i):
        answer_text = answer_text + "Votes: " + str(score[score.index(max(score), 0)]) + "\n" + str(href[score.index(max(score), 0)]) + "\n"
        href.pop(score.index(max(score), 0))
        score.pop(score.index(max(score), 0))
        i += 1
    return answer_text


def work_with_so():
    """
    This function works with Stack Overflow. First, it looks for answers on the user's request
    on the English version of Stack Overflow, than - on the Russian one
    Arguments:
        no arguments
    Returns:
        A string with an answer to be sent to the user by the bot
    """
    if g.user_request == "":
        return "Please, enter the request."
    # Looking for answers on Russian Stack Overflow
    g.lan = "English"
    score = []
    href = []
    make_a_request_for_questions("https://stackoverflow.com/questions?tab=votes&page=", score, href)
    answer_text_en = make_an_output(score, href)
    # Looking for answers on Russian Stack Overflow
    g.lan = "Russian"
    score = []
    href = []
    make_a_request_for_questions("https://ru.stackoverflow.com/questions?tab=votes&page=", score, href)
    answer_text_ru = make_an_output(score, href)
    return answer_text_en + "\n" + answer_text_ru
