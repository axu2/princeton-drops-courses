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
    url = "http://etcweb.princeton.edu/webfeeds/courseofferings/?fmt=json&term=current&subject=all"
    data = requests.get(url).json()['term'][0]['subjects']

    for dept in data:
        for course in dept['courses']:
            course_id = course['course_id']
            c = Course.objects(course_id=course_id).first()

            if not c:
                c = Course(course_id=course_id, 
                                dept=dept['code'], 
                                num=course['catalog_number'], 
                                title=course['title'])

            c.dates.append(date.today())
            c.enroll.append(int(course['enrollment']))

            if 'capacity' in course:
                c.max_enroll.append(course['capacity'])

            c.save()


if __name__ == '__main__':
    main()
    





