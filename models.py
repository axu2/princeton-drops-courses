from mongoengine import Document, IntField, StringField, ListField, DateField, connect
import requests
from bs4 import BeautifulSoup
from datetime import date
import os

host = os.getenv("MONGODB_URI")
connect("PrincetonDropsCourses", host=host)

class Course(Document):
    course_id = IntField()

    dept = StringField(max_length=3, min_length=3)
    num = StringField(max_length=4, min_length=3)

    title = StringField()

    dates = ListField(DateField())
    enroll = ListField(IntField(min_value=0))
    max_enroll = ListField(IntField(min_value=0))

    meta = {
        'indexes': [
            'course_id'
        ]
    }

def main(term="1194"):
    url = "https://registrar.princeton.edu/course-offerings/search_results.xml?submit=Search&term=" + term
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    for row in soup.table.findAll('tr')[1:]:
        cols = [list(col.stripped_strings) for col in row.findAll('td')]
        
        course_id = cols[0][0]

        try:
            course = Course.objects(course_id=course_id).first()
        except:
            dept, num = cols[1][0].split()
            course = Course(course_id=course_id, dept=dept, num=num, title=cols[2][0])

        course.dates.append(date.today())
        course.enroll.append(cols[8][0])

        if cols[9]:
            course.max_enroll.append(cols[9][0])

        course.save()

if __name__ == '__main__':
    main()
    





