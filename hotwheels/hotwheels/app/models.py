from django.db import models
from django.contrib.auth.models import User



class Car(models.Model):
    name = models.CharField(max_length=100)  # Car name
    description = models.TextField()         # Car description
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price in dollars
    image = models.ImageField(upload_to='cars/')  # Image of the car
    # created_at = models.DateTimeField(auto_now_add=True)  # When added
    stock = models.IntegerField()
    def __str__(self):
        return self.name  # Useful for admin display

class Wishlist(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
