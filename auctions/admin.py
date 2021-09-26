from django.contrib import admin
from .models import Comments, active_list, WatchList, Bid 

# Register your models here.
admin.site.register(Comments)
admin.site.register(active_list)
admin.site.register(WatchList)
admin.site.register(Bid)