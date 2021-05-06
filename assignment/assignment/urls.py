from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from apis import views
from django.contrib import admin

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('user/login/', views.LoginView.as_view()),
    path('user/register/', views.RegisterView.as_view()),
    path('admin/advisor/', views.AddAdvisorView.as_view()),
    path('user/<int:user_id>/advisor/', views.ListAdvisorView.as_view()),
    path('user/<int:user_id>/advisor/<int:advisor_id>/', views.AddBookingView.as_view()),
    path('user/<int:user_id>/advisor/booking/', views.ListBookingView.as_view()),
]
