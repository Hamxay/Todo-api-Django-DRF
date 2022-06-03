from rest_framework.response import Response
from rest_framework.decorators import api_view
from . serializer import TodoSerializer, RegisterSerializer, TodoPostSerializer
from .models import Todo
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.

class GetSingle(APIView):
    serializer_class = TodoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    allowed_methods = ('GET',)

    def get(self, request, pk, *args, **kwargs):
        get_all = {}
        try:
            get_all = Todo.objects.get(id=pk)
        except Exception as e:
            print("error", e)
            return Response({"Error": "This Todo not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializer(get_all)
        return Response(serializer.data)


class UpdateTodo(CreateAPIView):
    serializer_class = TodoPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    allowed_methods = ('PUT',)

    def put(self, request, pk, *args, **kwargs):
        get_all = {}
        try:
            get_all = Todo.objects.get(id=pk)
        except Exception as e:
            print("error", e)
            return Response({"Error": "This Todo not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TodoPostSerializer(instance=get_all,  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTodoByUserId(APIView):
    def get(self, request, pk, *args, **kwargs):
        get_all = Todo.objects.filter(user=pk)
        serializer = TodoSerializer(get_all, many=True)
        return Response(serializer.data)


class CreateTask(CreateAPIView):
    serializer_class = TodoPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    allowed_methods = ('POST',)

    def post(self, request):
        current_user = request.user.id
        data = request.data
        data['user'] = current_user

        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTodo(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    allowed_methods = ('DELETE',)

    def delete(self, request, pk):
        current_user = request.user.id
        get_all = {}
        try:
            get_all = Todo.objects.get(id=pk)
        except Exception as e:
            print("error", e)
            return Response({"Error": "This Todo not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializer(get_all)
        user_id = get_all.user.id

        if(current_user == user_id):
            get_all.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "Can't allow to delete this todo"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterUser(CreateAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    allowed_methods = ('POST',)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors
            print('Error', data.keys())
        return Response(data)


class SearchData(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
