from rest_framework import status, generics, exceptions as drf_exceptions
from rest_framework.response import Response

from .permissions import IsUserOwnerOfProject
from .serializers import TaskSerializer
from . import services


class CreateTaskAPIView(generics.CreateAPIView):

    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer
    permission_classes = (IsUserOwnerOfProject, )

    def get_queryset(self):
        return services.get_all_tasks()


class TaskCompletedAPIView(generics.GenericAPIView):
    """Make task completed, only task's performer can do"""

    def post(self, request, pk):
        if not services.is_user_task_performer(user=request.user, task_id=pk):
            raise drf_exceptions.PermissionDenied(
                {"detail": "Пользователь не является исполнителем таска"}
            )

        if services.check_task_completed(task_id=pk):
            raise drf_exceptions.ValidationError({"detail": "Таск уже выполнен"})

        if not services.check_task_deadline(task_id=pk):
            raise drf_exceptions.ValidationError({"detail": "Дедлайн уже прошел"})

        services.set_task_completed(task_id=pk)

        return Response(status=status.HTTP_200_OK)
