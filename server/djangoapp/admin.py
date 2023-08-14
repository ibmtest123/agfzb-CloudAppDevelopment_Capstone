from django.contrib import admin
from .models import CarModel, CarMake


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'type', 'year', 'dealer_id')

class CarModelInline(admin.TabularInline):  # You can also use StackedInline if you prefer
    model = CarModel
    extra = 1  

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

