from tkinter.ttk import Widget
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateInput

# Create your models here.


class Restaurent(models.Model):
    name = models.CharField(max_length=40)
    restaurent_pics = models.ImageField(upload_to = 'restaurent_pics', blank=True)
    total_seat = models.IntegerField()
    opening = models.CharField(max_length=10)
    closed = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}'

TIME_CHOICES =(
    ("10", "10:00 AM"),
    ("11", "11:00 AM"),
    ("12", "12:00 PM"),
    ("1", "1:00 PM"),
    ("2", "2:00 PM"),

)

STATUS_CHOICES =(
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
    ("Restore", "Restore"),

)
class Reservation(models.Model):
    restaurents = models.ForeignKey(Restaurent, on_delete=models.CASCADE, null=False, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person = models.IntegerField(default='1')
    booking_date = models.DateField(null=True)
    booking_time = models.CharField(choices=TIME_CHOICES, max_length=50, null=True)
    status = models.CharField(max_length=40,choices=STATUS_CHOICES,default='Pending')

    def __str__(self):
        return f'{self.restaurents.name} status {self.status}'

class Product(models.Model):
    restaurents = models.ForeignKey(Restaurent, on_delete=models.CASCADE, null=False, default='')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images')
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    image = models.ImageField(upload_to="product_images")
    product_name = models.CharField(max_length=50, null=True)
    product_id = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.CharField(max_length=1000, default="")
    quantity = models.CharField(max_length=50, null=True)
    total = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

class History(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    restaurent_id = models.CharField(max_length=100, null=True)
    product_id = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.order.product_name