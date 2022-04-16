from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import foodItems, foodStock


#* ex. /ffdb/
def index(request):
    all_food_items = foodItems.objects.all().order_by('foodName') # get all items & order alphabetically
    food_stock = foodStock.objects.all().order_by('foodItemss__foodName') # get all item's stock, ordered by name (same as all_food_items)

    #* handles search queries (and show all button)
    if request.method == 'GET':
        query = request.GET.get('q')
        
        if query == '*ShowAll': # "search" to reveal all items
            context = {
                'all_food_items': all_food_items,
                'query': query,
            }

        elif query != None: #verify that user searched for something
            search_results = foodItems.objects.filter(Q(foodName__icontains=query) | Q(foodLocation__iexact=query)).order_by('foodName') #retrieve query
            context = {
                'all_food_items': all_food_items,
                'search_results': search_results,
                'query': query,
            }

        else: # search has no results
            context = {
                'all_food_items': all_food_items,
                'food_stock': food_stock
            }
    
    #* new item creation from index form
    elif request.method =='POST' and request.POST.get('new_id') == 'new_index': # POST comes from index new item form
        # fetch values
        new_name = request.POST.get('Name')
        new_location = request.POST.get('Location')
        new_stock = request.POST.get('Number')
        new_notes = request.POST.get('Notes')

        # add to DB:
        new_item = foodItems(foodName=new_name, foodLocation=new_location, foodItemNotes=new_notes)
        new_item.save()
        new_item_stock = foodStock(foodLocation=new_location, stockNumber=new_stock)
        new_item_stock.save()
        new_item_stock.foodItemss.add(new_item)

        new_confirmation = "Item creation completed."

        context = {
            'all_food_items': all_food_items,
            'food_stock': food_stock,
            'new_confirmation': new_confirmation,
        }

    #* item deletion from detail form
    elif request.method == 'POST' and request.POST.get('deletion_id') == 'delete_detail': # POST comes from detail delete form
        # fetch values
        item_id = request.POST.get('item_id') # fetch pk of item to be deleted
        #! i think this is all i need to fetch - just the pk

        # delete from db
        delete_item = foodItems.objects.filter(pk=item_id) #item to be deleted
        delete_item_stock = foodStock.objects.filter(pk=item_id)
        delete_item.delete()
        delete_item_stock.delete()

        delete_confirmation = "Deletion completed."
        
        context = {
            'all_food_items': all_food_items,
            'food_stock': food_stock,
            'delete_confirmation': delete_confirmation,
        }

    else:
        context = {
            'all_food_items': all_food_items,
            'food_stock': food_stock,
            }

    return render(request, "ffdb/index.html", context)


#* ex. /ffdb/freezer/
def freezer(request):
    all_food_items_freezer = foodItems.objects.all()
    all_food_items_freezer_1 = foodItems.objects.filter(foodLocation__startswith='1') # gets a list of all items in the first freezer
    all_food_items_freezer_2 = foodItems.objects.filter(foodLocation__startswith='2') # gets a list of all items in the second freezer
    all_food_items_freezer_3 = foodItems.objects.filter(foodLocation__startswith='3') # gets a list of all items in the third freezer

    max_length = max(len(all_food_items_freezer_1), len(all_food_items_freezer_2), len(all_food_items_freezer_3)) # gets the max length for each freezer
    
    context = {
        'all_food_items_freezer': all_food_items_freezer,
        'all_food_items_freezer_1': all_food_items_freezer_1,
        'all_food_items_freezer_2': all_food_items_freezer_2,
        'all_food_items_freezer_3': all_food_items_freezer_3,
        'max_length': range(max_length),
    }
    
    return render(request, "ffdb/freezer.html", context)
   

#* ex. /ffdb/1/
def detail(request, foodItems_id):
    item = get_object_or_404(foodItems, pk=foodItems_id)
    stock = get_object_or_404(foodStock, pk=foodItems_id)
    fI_id = foodItems_id #allows the edit, deletion & stock forms to identify their item's primary key

    #* item edit/update from detail form
    if request.method == 'POST' and request.POST.get('edit_id') == 'edit_detail': # POST comes from detail edit form
        #* fetch values
        edit_name = request.POST.get('Name')
        edit_location = request.POST.get('Location')
        edit_stock = request.POST.get('Number')
        edit_notes = request.POST.get('Notes')
        item_id = request.POST.get('item_id')

        #* update db
        foodItems.objects.filter(pk=item_id).update(foodName=edit_name, foodLocation=edit_location, foodItemNotes=edit_notes)
        foodStock.objects.filter(pk=item_id).update(foodLocation=edit_location, stockNumber=edit_stock)
        
        edit_confirmation = "Edit completed, refresh to see changes." # confirmation

        context = {
            'item': item,
            'stock': stock,
            'fI_id': fI_id,
            'edit_confirmation': edit_confirmation,
        }

    #* stock update add from detail form
    elif request.method == 'POST' and request.POST.get('stock_id') == 'stockAdd_detail':
        #* fetch values
        add_stock = int(request.POST.get('stock_add')) + 1
        item_id = request.POST.get('item_id')

        if add_stock < 2147483648:
        #* update db
            foodStock.objects.filter(pk=item_id).update(stockNumber=add_stock)
            stock_confirmation = "Stock added, refresh to see changes." # confirmation

        else:
            stock_confirmation = "Number too big, stock not updated!"

        context = {
            'item': item,
            'stock': stock,
            'fI_id': fI_id,
            'stock_confirmation': stock_confirmation
        }

    #* stock update remove from detail form
    elif request.method == 'POST' and request.POST.get('stock_id') == 'stockRemove_detail':
        #* fetch values
        remove_stock = int(request.POST.get('stock_remove')) - 1
        item_id = request.POST.get('item_id')

        if remove_stock >= 0:
        #* update db
            foodStock.objects.filter(pk=item_id).update(stockNumber=remove_stock)
            stock_confirmation = "Stock removed, refresh to see changes." # confirmation

        else:
            stock_confirmation = "Number too small, stock not updated!"

        context = {
            'item': item,
            'stock': stock,
            'fI_id': fI_id,
            'stock_confirmation': stock_confirmation
        }

    else:
        context = {
            'item': item, 
            'stock': stock, 
            'fI_id': fI_id,
            }
    
    return render(request, "ffdb/detail.html", context)


# mostly covered on detail, will use image on location page.
#* ex. /ffdb/1/location
def location(request, foodItems_id):
    item = get_object_or_404(foodItems, pk=foodItems_id)
    
    location_qs = str(foodItems.objects.filter(pk=foodItems_id).values('foodLocation'))
    location_id = location_qs[29:32] # ex. 2.1 or 3.2 ect
    location = "ffdb/%s.png" % location_id

    context = {
        'item': item,
        'location': location,
    }

    return render(request, "ffdb/location.html", context)
