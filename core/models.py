from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

#user model
class User(AbstractUser):
    pass



# book model
class Book(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=70)
    price = models.IntegerField()
    pages = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.category} - {self.price} - {self.pages} - {self.user}"



