from django.db import models

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