from django.db import models
from datetime import datetime

# Create your models here.
class RFIDChipReader(models.Model):
    cardID = models.CharField(max_length=255)
    authorised = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
            super(RFIDChipReader, self).save(*args, **kwargs)