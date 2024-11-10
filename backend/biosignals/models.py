from datetime import timezone

from django.db import models

class BioSignals(models.Model):
    user_id = models.CharField(max_length=50)
    signal_data = models.JSONField()
    sleep_stage = models.CharField(max_length=50)  # 睡眠阶段标签
    timestamp = models.DateTimeField(null=True)


    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['user_id']),
        ]
