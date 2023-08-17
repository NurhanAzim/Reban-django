from django.contrib import admin

from .models import Chicken, Egg, EggShipment

@admin.register(Chicken)
class ChickenAdmin(admin.ModelAdmin):
    pass

@admin.register(Egg)
class EggAdmin(admin.ModelAdmin):
    list_display = ['collection_date', 'size', 'owner', 'egg_shipment']
    actions = ['nullify_shipment']

    @admin.action(description='Mark selected eggs\'s shipment as Null')
    def nullify_shipment(self, request, queryset):
        updated = queryset.update(egg_shipment=None)
        self.message_user(request, f'{updated} eggs\'s shipment was nullified', level='SUCCESS')

@admin.register(EggShipment)
class EggShipmentAdmin(admin.ModelAdmin):
    list_display = ('date_shipped', 'customer', 'owner')
