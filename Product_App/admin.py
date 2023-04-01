from django.contrib import admin

from Product_App.models import History, Order, Product, Reservation, Restaurent

# Register your models here.
admin.site.register(Restaurent)
admin.site.register(Reservation)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(History)

