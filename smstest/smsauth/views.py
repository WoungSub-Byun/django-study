import json
import random
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SmsAuth

# Create your views here.


class SMSCheckView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            code = "123456"
            SmsAuth.objects.update_or_create(
                send_to=data["phone_number"], auth_code=code
            )
            SmsAuth.send_sms()
            return Response({"message": "OK"}, status=200)
        except KeyError:
            return Response({"message": "Bad Request"}, status=400)

    def get(self, request):
        try:
            phone_number = request.query_params["phone_number"]
            auth_code = request.query_params["auth_code"]
            result = SmsAuth.check_auth_number(phone_number, auth_code)
            return Response({"message": "OK", "result": result})
        except KeyError:
            return Response({"message": "Bad request"}, status=400)
