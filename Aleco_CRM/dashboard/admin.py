from django.contrib import admin
from .models import *

admin.site.register(Projects)
admin.site.register(Inventory)
admin.site.register(Progress)
admin.site.register(InventoryHistory)
admin.site.register(MaintenanceMode)
admin.site.register(RecentActivity)
