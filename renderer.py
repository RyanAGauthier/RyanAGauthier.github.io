from os import listdir, path
from jinja2 import Environment, select_autoescape, FileSystemLoader
from dateutil import parser
from datetime import datetime, timedelta

env = Environment(
    loader=FileSystemLoader(),
    autoescape=select_autoescape()
)
class myFolder:
    def __init__(self, href, caption):
        self.href = href
        self.caption = caption

resume = ""
latestResumeDate = datetime.min
myList = []
# {% for item in navigation %}
#         						<li><a href="{{ item.href }}">{{ item.caption }}</a></li>
# Load all the filenames, then identify the most recent resume...
for ele in listdir():
    currentPath = path.join(".", ele)
    if path.isdir(currentPath):
        folder = myFolder(ele,ele)
        myList.append(folder)
    elif path.isfile(currentPath) and "Resume" in ele:
        if parser.parse(ele) > latestResumeDate:
            resume = ele
template = env.get_template("index.html.jinja2")
outfile = template.render(navigation = myList, latest_resume = resume)
with open("index.html", "w") as fh:
    fh.write(outfile)
# print("Hello, World!")
# print(listdir())