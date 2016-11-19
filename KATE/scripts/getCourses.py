import json
from pprint import pprint
from kateapp.models import Classes, Courses, People, Term, Courses_Term, Courses_Classes

with open('data.json') as data_file:    
    data = json.load(data_file)
for i in range(len(data)):
  course = data[i]
  code = course["code"]

  c = Courses(code, title = course["title"], lecturer = People.objects.get(login="test01"))
  c.save()

  terms = course["term"].split(',')
  for t in terms:
	course_term = Courses_Term(code=c, term=Term.objects.get(term=int(t)))
	course_term.save()

  course_class = Courses_Classes(code=c, letter_yr=Classes.objects.get(letter_yr="c1"))
  course_class.save()
