from django.db import models


class Patient(models.Model):
    sr_no = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=-1)
    sex = models.CharField(max_length=20)
    patient_status = models.CharField(max_length=20)
    hospitalization_status = models.CharField(max_length=20)
    ward = models.CharField(max_length=200)
    sample_result = models.CharField(max_length=20)
    testing_lab = models.CharField(max_length=200)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.name, self.sex, self.patient_status, self.hospitalization_status,
                                          self.sample_result, self.ward)


class IncomingFile(models.Model):
    file = models.FileField(upload_to='validate_data/incoming/')
