from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Farmer)
admin.site.register(Pivot)
admin.site.register(Harvest)
admin.site.register(Input)
