
from django.urls import path

from .views import MyProfile, SignUpView

app_name = 'account'

urlpatterns = [
    path('my_profile/', MyProfile.as_view(), name='my_profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
