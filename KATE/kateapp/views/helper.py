from django.db.models import Max

def get_next_exercise_number(exercises):
    nextNumber = exercises.aggregate(Max('number'))['number__max']
    nextNumber = 1 if nextNumber is None else nextNumber + 1
    return nextNumber
