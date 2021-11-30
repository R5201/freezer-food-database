from django import http
from django import template
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import context, loader

from .models import foodItems

# ex. /ffdb/
def index(request):
    all_food_items = foodItems.objects.all()
    template = loader.get_template('ffdb/index.html')
    context = {'all_food_items': all_food_items}
    return HttpResponse(template.render(context, request))
    
    #//return render(request, 'ffdb/index.html', context))
    #//return HttpResponse("Hello, world. Welcome to the FFDB index")

# ex. /ffdb/1/
def detail(request, foodItems_id):
    item = get_object_or_404(foodItems, pk=foodItems_id)
    #//template = loader.get_template('ffdb/detail.html')
    #//context = {
    #//    'item': item,    
    #//}
    return render(request, "ffdb/detail.html", {'item': item})
    #//return HttpResponse(template.render(context, request))

    #//return HttpResponse("You're looking at food item %s." % foodItems_id)

# mostly covered on detail, will use image on location page.
# /ffdb/1/location
def location(request, foodItems_id):
    item = get_object_or_404(foodItems, pk=foodItems_id)
    #//template = loader.get_template('ffdb/location.html')
    #//context = {
    #//    'item': item,    
    #//}
    return render(request, "ffdb/location.html", {'item': item})
    #//return HttpResponse(template.render(context, request))
    
    #//response = "You're looking at the location of food item %s."
    #//return HttpResponse(response % foodItems_id)

#// ? might not need/want this one, could just be done on the detail page, idk
#// /ffdb/1/notes
#//def notes(request, foodItems_id):
    #//return HttpResponse("You're looking at the notes of food item %s." % foodItems_id)