from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from apis import views
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('user/register', views.UserList.as_view(),name='register'),
    path('user/login', views.UserList.as_view(),name='login'),
    path('admin/advisors/', views.AdvisorList.as_view()),
]
