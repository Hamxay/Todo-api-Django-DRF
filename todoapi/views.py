from rest_framework.response import Response
from rest_framework.decorators import api_view
from . serializer import TodoSerializer, RegisterSerializer, TodoPostSerializer
from .models import Todo
from rest_framework.generics import ListAPIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes

# Create your views here.


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllTodos(request):
    get_all = Todo.objects.all()
    serializer = TodoSerializer(get_all, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSingle(request, pk, *args, **kwargs):
    get_all = Todo.objects.get(id=pk)
    serializer = TodoSerializer(get_all)
    return Response(serializer.data)


@swagger_auto_schema("PATCH", request_body=TodoPostSerializer, responses={200: TodoSerializer})
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UpdateTodo(request, pk, *args, **kwargs):
    get_all = Todo.objects.get(id=pk)
    serializer = TodoPostSerializer(instance=get_all,  data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getDataByUser(request, pk, *args, **kwargs):
    get_all = Todo.objects.filter(user=pk)
    serializer = TodoSerializer(get_all, many=True)
    return Response(serializer.data)


@swagger_auto_schema("POST", request_body=TodoPostSerializer, responses={200: TodoSerializer})
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def taskCreate(request):
    current_user = request.user.id
    data = request.data
    data['user'] = current_user

    serializer = TodoSerializer(data=data)
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
