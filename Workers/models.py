from django.db import models


# Create your models here.
class Worker(models.Model):
    Worker_id = models.BigAutoField
    Worker_name = models.CharField(max_length=60)
    Worker_company = models.CharField(max_length=60)
    Worker_ptype = models.CharField(default="Carpenter", max_length=20)
    Worker_work_profile_id = models.CharField(default="fls", max_length=30)
    Worker_description = models.CharField(max_length=1500)
    Worker_price = models.IntegerField()

    def __str__(self):
        return self.Worker_work_profile_id + " : " + str(self.Worker_name)
