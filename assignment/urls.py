from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from apis import views
from django.contrib import admin

urlpatterns = [
    path('user/login/', views.UserView.as_view()), # login api - get
    path('user/register/', views.UserView.as_view()), # register - post
    path('admin/advisor/', views.AddAdvisorView.as_view()), # add advisor - post
    path('user/<int:user_id>/advisor/', views.ListAdvisorView.as_view()), # list advisors - get
    path('user/<int:user_id>/advisor/<int:advisor_id>/', views.BookingView.as_view()), # list bookings - get
    path('user/<int:user_id>/advisor/booking/', views.BookingView.as_view()), # make booking - post
    path('', views.init_view),
]
