from django.db import models

# Create your models here.


class WorkDate(models.Model):
    id = models.IntegerField(primary_key=True)
    name_id = models.IntegerField()
    name = models.CharField(max_length=255)
    firsttime = models.TimeField()
    lasttime = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta():
        db_table = 'cashierwork'


class AdminDate(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    datetime = models.DateField()

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta():
        db_table = 'admin'


class CashierDate(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    datetime = models.DateField()

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta():
        db_table = 'cashier'
