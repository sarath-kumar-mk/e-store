from django.contrib import admin
from core.models import *

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(CheckoutAddress)
admin.site.register(Contact)
admin.site.register(SentMsg)

# Register your models here.
