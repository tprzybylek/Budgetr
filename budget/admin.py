from django.contrib import admin
from .models import Category, Budget, Operation

# Register your models here.

admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Operation)
