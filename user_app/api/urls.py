from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path,include
from user_app.api.views import registration_view,logout_view
urlpatterns = [
    path('login/',obtain_auth_token,name='login'),
    path('register/',registration_view,name='registration'),
    path('logout/',logout_view,name='logout')


]


