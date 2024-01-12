from django.contrib import admin
from .models import *
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'college', 'building')
    list_filter = ('college', 'building', 'room_type')
    search_fields = ['name']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('college', 'building', 'name')
        return queryset
class EquipmentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('name')
        return queryset
    
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_filter = ('id', 'name', 'slug')
    search_fields = ['name']

# Register your models here.
admin.site.register(College,CollegeAdmin)
admin.site.register(CollegeCode)
admin.site.register(Department)
admin.site.register(Building)
admin.site.register(RoomType)
admin.site.register(Room, RoomAdmin)
admin.site.register(Term)
admin.site.register(Schedule)
admin.site.register(ScheduleFile)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Contact)
admin.site.register(ScheduleExtra)