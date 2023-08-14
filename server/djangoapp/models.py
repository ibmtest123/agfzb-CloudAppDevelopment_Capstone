from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class CarModel(models.Model):
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.PositiveIntegerField() 
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CAR_TYPES)
    year = models.DateField()

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year})"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
