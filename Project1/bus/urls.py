from django.urls import path
from .  import views


urlpatterns = [
    path('', views.home, name= "home"),
    path('register', views.register, name= "register"),
    path('route/<result>', views.route, name="route"),
    path('book/<int:id>', views.book, name="book"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('reciept', views.reciept, name="reciept")
]