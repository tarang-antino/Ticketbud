"""EventManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from event import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('user/',views.UserList.as_view()),
    path('user/<int:pk>',views.UserDetails.as_view()),
    # path('user/',views.UserDetails.as_view()),  #used for directly accessing the user through token
    path('userLogin/',views.UserLogin.as_view()),
    path('Event/',views.EventList.as_view()),
    path('Event/<int:pk>',views.EventDetails.as_view()),
    path('eventRes/<int:pk>',views.EventRes.as_view()),
    path('eventbook/<int:pk>',views.Event_Book.as_view()),
    path('updatepassword/<int:pk>',views.UpdatePassword.as_view()),
]
