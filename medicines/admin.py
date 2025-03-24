from django.contrib import admin

from medicines.models import InventoryItem, InventoryStock, InventoryTransaction

# Register your models here.
admin.site.register(
    InventoryItem,
)
admin.site.register(
    InventoryTransaction,
)

@admin.register(InventoryStock)
class InventoryStockAdmin(admin.ModelAdmin):
    list_display = ("item", "expiration_date", "count", "date_of_delivery")
    list_filter = ("expiration_date",)
    search_fields = ("item__name",)
