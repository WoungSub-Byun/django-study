from django.urls import path
from .views import *

urlpatterns = [path("/smsauth", SMSCheckView.as_view(), name="smscheckview")]
