from django.db import models

# Create your models here.
class SmsAuth(models.Model):
    send_to = models.CharField(verbose_name="send_to", max_length=11)
    auth_code = models.CharField(verbose_name="auth_code", max_length=6)
    created_at = models.DateTimeField(verbose_name="created_at", auto_now=True)

    class Meta:
        db_table = "SMSAUTH"
