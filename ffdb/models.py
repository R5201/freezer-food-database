import datetime
from django.db import models
from django.db.models.base import Model
from django.utils import timezone

#* Create your models here.

#* 
class foodItems(models.Model):
    foodName = models.CharField('the name of the food item', max_length=200)
    foodLocation = models.CharField('the location of the food item', max_length=3)
    foodItemNotes = models.CharField('any other notes about the food item', max_length=300, blank=True)
    #//edited = models.DateTimeField('date edited')
    def __str__(self):
        return self.foodName


#* Many food items can have many locations
class foodStock(models.Model):
    #//foodItemsId = models.ForeignKey(foodItems, on_delete=models.CASCADE) 
    foodLocation = models.CharField('the location of the food item', max_length=3)
    stockNumber = models.PositiveIntegerField('the number of food items')
    foodItemss = models.ManyToManyField(foodItems)
    def __str__(self):
        name_str = str(foodItems.objects.filter(pk=self.id))
        return name_str[23:-3] + "'s stock"