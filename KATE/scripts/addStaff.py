from kateapp.models import People, Classes

staff = People(login="test01", firstname="Bob", lastname="Smith")
staff.save()
