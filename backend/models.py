from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    def __str__(self):
        return self.user_id


class Avans(models.Model):
    user = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.amount}"
    

class AskMoney(models.Model):
    client = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True, auto_now_add=False)
    amount = models.IntegerField(null=True)


class Payment(models.Model):
    payment = models.CharField(max_length=200, null=True, blank=True)
    date = models.CharField(max_length=200, null=True, blank=True)
    amount = models.IntegerField()
