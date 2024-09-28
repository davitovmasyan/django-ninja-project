import factory
import random

from django.contrib.auth import get_user_model

from .models import Invitation


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_verified = factory.LazyAttribute(lambda o: random.choice([True, False]))

    is_staff = False
    is_superuser = False

    class Meta:
        model = get_user_model()
