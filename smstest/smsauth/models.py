from django.db import models
import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json
from django.conf import settings

# Create your models here.
class SmsAuth(models.Model):
    send_to = models.CharField(verbose_name="send_to", max_length=11)
    auth_code = models.CharField(verbose_name="auth_code", max_length=6)
    created_at = models.DateTimeField(verbose_name="created_at", auto_now=True)

    class Meta:
        db_table = "SMSAUTH"

    def is_expired(self, auth_code):
        now = datetime.now()
        obj = SmsAuth.objects.get(auth_code=auth_code)
        if (
            now - obj.created_at
        ).seconds > 180:  # datetime연산은 timedelta 값으로 반환, 인증만료시간 3분
            return True
        return False

    def check_auth_number(self, phone_number, auth_code):
        obj = self.objects.get(phone_number=phone_number, auth_code=auth_code)
        if obj.exists():
            return True
        return False

    def make_signature(self, string):
        secret_key = bytes(settings.API_SECRET_KEY, "UTF-8")
        signingKey = base64.b64encode(
            hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
        )
        return signingKey

    def send_sms(self):
        timestamp = str(int(time.time() * 1000))
        uri = "sms/v2/services/{}/messages".format(settings.SMS_SERVICE_ID)
        message = "POST " + uri + "\n" + timestamp + "\n" + settings.API_ACCESS_KEY
        message = bytes(message, "UTF-8")

        signature = self.make_signature(message)

        headers = {
            "Content-type": "application/json; charset=UTF-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": settings.API_ACCESS_KEY,
            "x-ncp-apigw-signature-v2": signature,
        }
        body = {
            "type": "SMS",
            "contentType": "COMM",
            "from": settings.SMS_SEND_PHONE_NUMBER,
            "content": "[django-test] 인증 번호 [{}]를 입력해주세요".format(self.auth_code),
            "messages": [{"to": self.send_to}],
        }
        requests.post(settings.API_URL, data=json.dumps(body), headers=headers)