from django.contrib import admin
from .models import Room, Electricity, House, Guests, Personnel
# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ['house', 'roomsNumber', 'acreage']
    list_filter = ['house' ,'acreage']
    search_fields = ['roomsNumber', 'acreage']


admin.site.register(Room, RoomAdmin)

class GuestsAdmin(admin.ModelAdmin):
    list_display = ['room', 'fullname']
    list_filter = ['room']
    search_fields = ['room', 'fullname']

class ElectricityAdmin(admin.ModelAdmin):
    list_display = ['room', 'index_electricity', 'date']
    list_filter = ['room']
   
admin.site.register(Electricity, ElectricityAdmin)

class HouseAdmin(admin.ModelAdmin):
    list_display = ['nameHouse', 'address']
    list_filter = ['nameHouse']
    search_fields = ['nameHouse']

admin.site.register(House, HouseAdmin)

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ['id_personnel', 'fullname', 'phone']
    list_filter = ['id_personnel' ,'fullname']
    search_fields = ['id_personnel','fullname']

admin.site.register(Personnel, PersonnelAdmin)