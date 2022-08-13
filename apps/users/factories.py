import factory
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.fr")
    phone = factory.Sequence(lambda n: f"{n}" * 10)
    password = factory.PostGenerationMethodCall('set_password', 'default')
