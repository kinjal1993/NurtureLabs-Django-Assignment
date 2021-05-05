from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from apis import views
from django.contrib import admin

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view()),
    path('admin/advisors/', views.AdvisorList.as_view()),
]


