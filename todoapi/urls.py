from django.urls import path,  re_path
from django.conf.urls import url
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
    openapi.Info(
        title="Todoapp API",
        default_version='v1',
        description="Test description",
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r'^swagger(?P<format>\.json|\.yaml)$',
         schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path('get_all', views.getAllTodos, name='test'),
    path('get/<str:pk>', views.getSingle, name='get_single'),
    path('get_by_user<str:pk>', views.getDataByUser, name='get_by_user'),
    path('update/<str:pk>', views.UpdateTodo, name='get_update'),
    path('add_todo', views.taskCreate, name='add_todo'),
    path('delete_todo/<str:pk>', views.RemoveTodo, name='remove todo'),
    path('register', views.register_view, name='register'),
    path("find_todo/<str:title>/<str:description>",
         views.search_in_todo, name='find'),

    path('get', views.SearchData.as_view(), name='Search Data')
]
