from django.db import models
from location_field.models.plain import PlainLocationField
from django.db.models import Sum

#Creates Industry model for database
class Industry(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

#Creates Funding model for database
class Funding(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

#Creates Company model for database
class Company(models.Model):
    name = models.CharField(max_length=100)
    overview = models.TextField(default='')
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING)
    location = PlainLocationField(based_fields=['city'], zoom=2)

    def __str__(self):
        return self.name

#Creates Deal model for database
class Deal(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    investor = models.CharField(default='', max_length=100)
    funding = models.ForeignKey(Funding, on_delete=models.DO_NOTHING)
    date = models.DateField(null=True, blank=True)
    funding_amount = models.IntegerField()

    def __str__(self):
        return self.company.name
