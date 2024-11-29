from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatbot, name="chatbot"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("employee", views.employee, name="employee"),
    path("employee_sync", views.employee_sync, name="employee_sync"),
    path("employee_async", views.employee_async, name="employee_async"),
]
