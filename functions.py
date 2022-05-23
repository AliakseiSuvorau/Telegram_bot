from bs4 import BeautifulSoup  # for scrapping the information
import Globals as g
import requests  # for sending requests and getting html


def to_url(request):
    """
    This function translates the string with the request to the url code
    Arguments:
        request: the string with request
    Returns:
        The string with url
    """
    url = ""
    for i in range(len(request)):
        if request[i] == "!":
            url += "%21"
        elif request[i] == "\"":
            url += "%22"
        elif request[i] == "#":
            url += "%23"
        elif request[i] == "$":
            url += "%24"
        elif request[i] == "%":
            url += "%25"
        elif request[i] == "&":
            url += "%26"
        elif request[i] == "'":
            url += "%27"
        elif request[i] == "(":
            url += "%28"
        elif request[i] == ")":
            url += "%29"
        elif request[i] == "+":
            url += "%2B"
        elif request[i] == ",":
            url += "%2C"
        elif request[i] == "/":
            url += "%2F"
        elif request[i] == ":":
            url += "%3A"
        elif request[i] == ";":
            url += "%3B"
        elif request[i] == "=":
            url += "%3D"
        elif request[i] == "%":
            url += "%3F"
        elif request[i] == "@":
            url += "%40"
        elif request[i] == "[":
            url += "%5B"
        elif request[i] == "\\":
            url += "%5C"
        elif request[i] == "]":
            url += "%5D"
        elif request[i] == "^":
            url += "%5E"
        elif request[i] == "`":
            url += "%60"
        elif request[i] == "{":
            url += "%7B"
        elif request[i] == "|":
            url += "%7C"
        elif request[i] == "}":
            url += "%7D"
        elif request[i] == " ":
            url += "+"
        else:
            url += request[i]
    return url


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
    questions = []
    url = base_url + g.user_request
    if g.tagged:
        url += "?tab=Votes"
    response = requests.get(url)  # getting request from the site with the html
    html = BeautifulSoup(response.text, 'html.parser')
    if g.tagged:
        question_data = html.find_all('div', class_="s-post-summary js-post-summary")
    else:
        question_data = html.find_all('div', class_="question-summary search-result")
    if question_data:
        questions.extend(question_data)
    look_for_answers(questions, score, href)


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
            if g.tagged:
                score.append(int(item.find('span', {"class": "s-post-summary--stats-item-number"}).text))
            else:
                score.append(int(item.find('strong').text))
            if g.lan == "English":
                href.append("https://stackoverflow.com" + item.a.get('href'))
            else:
                href.append("https://ru.stackoverflow.com" + item.a.get('href'))
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
            return "No answers found on English Stack Overflow. The site may have asked you to pass captcha.\n"
        else:
            return "No answers found on Russian Stack Overflow.\n"
    i = 0
    while i < min(g.num_of_results, len(score) + i):
        answer_text = answer_text + "Votes: " + str(score[score.index(max(score), 0)]) + "\n" + str(href[score.index(max(score), 0)]) + "\n"
        href.pop(score.index(max(score), 0))
        score.pop(score.index(max(score), 0))
        i += 1
    return answer_text


def tag_check():
    """
    This function checks if the request suits most popular tags
    Arguments:
        Nothing.
    Returns:
        True if the request suits one of the tags and False if it doesn't
    """
    if g.user_request == "javascript" or g.user_request == "python" or g.user_request == "php":
        return True
    elif g.user_request == "java" or g.user_request == "html" or g.user_request == "android":
        return True
    elif g.user_request == "c++" or g.user_request == "css" or g.user_request == "jquery":
        return True
    elif g.user_request == "python-3.x" or g.user_request == "mysql" or g.user_request == "sql":
        return True
    elif g.user_request == "c" or g.user_request == "linux" or g.user_request == "json":
        return True
    elif g.user_request == "windows" or g.user_request == "ubuntu" or g.user_request == "delphi":
        return True
    elif g.user_request == "node.js" or g.user_request == "arrays" or g.user_request == "excel":
        return True
    return False


def work_with_so():
    """
    This function works with Stack Overflow. First, it looks for answers on the user's request
    on the English version of Stack Overflow, than - on the Russian one
    Arguments:
        No arguments.
    Returns:
        A string with an answer to be sent to the user by the bot
    """
    if g.user_request == "":
        return "Please, enter the request."
    if tag_check():
        g.tagged = 1
        url_en = "https://stackoverflow.com/questions/tagged/"
        url_ru = "https://ru.stackoverflow.com/questions/tagged/"
    else:
        url_en = "https://stackoverflow.com/search?q="
        url_ru = "https://ru.stackoverflow.com/search?q="
    g.user_request = to_url(g.user_request)
    # Looking for answers on Russian Stack Overflow
    g.lan = "English"
    score = []
    href = []
    make_a_request_for_questions(url_en, score, href)
    answer_text_en = make_an_output(score, href)
    # Looking for answers on Russian Stack Overflow
    g.lan = "Russian"
    score = []
    href = []
    make_a_request_for_questions(url_ru, score, href)
    answer_text_ru = make_an_output(score, href)
    g.tagged = 0
    return answer_text_en + "\n" + answer_text_ru
