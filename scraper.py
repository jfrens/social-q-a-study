from bs4 import BeautifulSoup
import urllib.request
import sys

if len(sys.argv) != 2:
    print("Error: the username was not specified", file=sys.stderr)
    sys.exit()

username = sys.argv[1]

print("Scraping data for user:" + username)

url = 'http://brainly.com/profile/' + username + '/solved'

# Build the request
# Brainly forbids requests without the User-Agent header
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

# Send the request and get back a big blob of Unicode HTML
req = urllib.request.Request(url, None, headers)
with urllib.request.urlopen(req) as response:
   the_page = response.read()

# Pass the html to the BeautifulSoup parser
soup = BeautifulSoup(the_page, "html.parser")

# Ensure we landed on a profile page
if not soup.head.title.string.startswith("Brainly.com - User's profile"):
    print("Error: did not land on a profile page")
    sys.exit()

# The list of questions has an ol tag, so here we search for all such elements
for ol in soup.body.find_all('ol'):
    if ol['class'][0].startswith("tasks-list"):
        soup_tasks = ol

# Build a list of question urls that the user has responded
question_list = []
for div in soup_tasks.find_all('div'):
    if div['class'][0].startswith("task-content"):
        soup_question = div.find('a')
        question_list.append(soup_question['href'])

# Parse the info for each question
for question_urlpart in question_list:
    question_url = 'http://brainly.com' + question_urlpart

    # Send the request and get back a big blob of Unicode HTML
    req = urllib.request.Request(question_url, None, headers)
    with urllib.request.urlopen(req) as response:
       the_page = response.read()
    # Pass the html to the BeautifulSoup parser
    soup = BeautifulSoup(the_page, "html.parser")

    # Find the question
    question_text = ''
    for string in soup.body.find('h1', class_="sg-text").strings:
        question_text += string
    question_text = question_text.strip()

    answer_text = ''
    # Find the answer
    for section in soup.body.find_all(id="answers"):
        for answer in section.find_all(class_="brn-answer"):
            answerer = answer.find('a')['title']
            answer_element = answer.find(class_="sg-text")
            if (username.startswith(answerer)):
                for string in answer_element.strings:
                    answer_text += string
                answer_text = answer_text.strip()

    print("\n")
    print("Question: " + question_urlpart)
    print(question_text.encode("utf-8"))
    print("Answer: ")
    print(answer_text.encode("utf-8"))
