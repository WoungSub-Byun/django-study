from django.urls import path
from .views import *

urlpatterns = [path("", send_sms(), name="send_sms_func")]
