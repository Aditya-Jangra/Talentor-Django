from django.contrib.auth.models import User
from app.models import Person,LinkedinProfile


def fetchUserByEmail(user_email):
    try:
        return User.objects.filter(email=user_email).first()
    except Exception as e:
        return False


def get_people():
    people = Person.objects.all().values()
    return list(people)



def get_linked_in_profiles():
    linkedin_data = LinkedinProfile.objects.all().values()
    return list(linkedin_data)



def create_person(person_data):
    person = Person(**person_data)
    person.save()
    return person.id


def update_person_data(person_id, person_data):
    person = Person.objects.get(id=person_id)
    for key, value in person_data.items():
        setattr(person, key, value)
    person.save()


def delete_person(person_id):
    person = Person.objects.get(id=person_id)
    person.delete()
