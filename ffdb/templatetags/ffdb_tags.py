from django import template
register = template.Library()

@register.filter # custom filter that takes the current for loop index (or other index variable) and uses it to get the value (this cannot be done normally)
def index(indexable, i):
    try:
        return indexable[i]
    except: # if the index doesn't exist, then return nothing
        return ''