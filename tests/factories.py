from factory.django import DjangoModelFactory
from factory import Faker, SubFactory


class UserFactory(DjangoModelFactory):

    class Meta:
        model = 'users.User'

    username = Faker('user_name')
    email = Faker('email')
    password = 'password'
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = 'projects.Project'

    name = Faker('word')
    description = Faker('text')
    owner = SubFactory(UserFactory)


class TaskFactory(DjangoModelFactory):

    class Meta:
        model = 'tasks.Task'

    name = Faker('word')
    description = Faker('text')
    project = SubFactory(ProjectFactory)
    performer = SubFactory(UserFactory)
    deadline = Faker('date_time')
