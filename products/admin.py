from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Product,Category 


admin.site.register(Category)

admin.site.register(Product)