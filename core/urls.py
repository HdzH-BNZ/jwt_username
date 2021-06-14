from django.urls import path
from django.urls.resolvers import URLPattern

# on appelle les views créées dans le views.py
from .views import RegisterView, LoginView, UserView, LogOutView, getJoueurs

urlpatterns = [
    path('register/', RegisterView, name="RegisterView"),
    path('login/', LoginView, name="LoginView"),
    path('user/', UserView, name="UserView"),
    path('logout/', LogOutView, name="LogOutView"),
    path('joueurs/', getJoueurs, name="getJoueurs"),
]