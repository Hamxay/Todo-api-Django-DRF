from rest_framework.response import Response
from rest_framework.decorators import api_view
from . serializer import TodoSerializer, RegisterSerializer
from .models import Todo
from rest_framework.generics import ListAPIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from todoapi import serializer

# Create your views here.


@api_view(['GET'])
def getAllTodos(request):
    get_all = Todo.objects.all()
    serializer = TodoSerializer(get_all, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSingle(request, pk, *args, **kwargs):
    get_all = Todo.objects.get(id=pk)
    serializer = TodoSerializer(get_all)
    return Response(serializer.data)


# @api_view(['GET'])
# def getSearch(request, text):
#     get_all = Todo.objects.all()
#     serializer_class = TodoSerializer(get_all, many=True)
#     filter_backends = [SearchFilter]
#     search_fields = ['title', 'description']
#     return Response(serializer_class.data)


@swagger_auto_schema("POST", request_body=TodoSerializer, responses={200: TodoSerializer})
@api_view(['POST'])
def UpdateTodo(request, pk, *args, **kwargs):
    get_all = Todo.objects.get(id=pk)
    serializer = TodoSerializer(instance=get_all,  data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getDataByUser(request, pk, *args, **kwargs):
    get_all = Todo.objects.filter(user=pk)
    serializer = TodoSerializer(get_all, many=True)
    return Response(serializer.data)


@swagger_auto_schema("POST", request_body=TodoSerializer, responses={200: TodoSerializer})
@api_view(['POST'])
def taskCreate(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema("GET", request_body=TodoSerializer, responses={200: TodoSerializer})
@api_view(['GET'])
def search_in_todo(request, title, description):
    get_all = Todo.objects.filter(title=title, description=description)
    serializer = TodoSerializer(get_all, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def RemoveTodo(request, pk):
    get_all = Todo.objects.get(id=pk)
    serializer = TodoSerializer(get_all)
    get_all.delete()
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema("POST", request_body=RegisterSerializer, responses={200: RegisterSerializer})
@api_view(['POST'])
def register_view(request):
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
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
