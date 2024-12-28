from django.db import models
from UserAndAccessManagement.models import CustomUser
from uuid import uuid4
# Create your models here.


class PatientDetails(models.Model):
    patient_ID = models.UUIDField(default=uuid4,primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)


    class Meta:
        db_table = 'patient_details'