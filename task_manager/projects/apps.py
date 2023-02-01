from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task_manager.projects"

    def ready(self):
        import task_manager.projects.signals # noqa
