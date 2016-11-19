from kateapp.models import Term

t1 = Term(term=1, name="Autumn Term")
t2 = Term(term=2, name="Spring Term")
t3 = Term(term=3, name="Summer Term")
t1.save()
t2.save()
t3.save()
