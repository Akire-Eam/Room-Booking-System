from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
from bookingapp.models import Booking
from django.db.models import Exists, OuterRef
class HasBookingFilter(admin.SimpleListFilter):
    title = 'Has Booking'
    parameter_name = 'has_booking'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.annotate(has_booking=Exists(Booking.objects.filter(faculty__user=OuterRef('pk')))).filter(has_booking=True)
        elif self.value() == 'no':
            return queryset.annotate(has_booking=Exists(Booking.objects.filter(faculty__user=OuterRef('pk')))).filter(has_booking=False)

class CustomUserAdmin(UserAdmin):
    search_fields = ['email','first_name','last_name']
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_active', 'last_login',HasBookingFilter)
    fieldsets = (
        (None, {'fields': ('username', 'password','college','department','user_type')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'can_book', 'can_approve', 'can_remark', 'can_manage_equipment',
                       'can_manage_facilities', 'can_manage_terms', 'can_upload_schedules',
                       'can_view_bookings')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
class ReferenceAcc(admin.ModelAdmin):
    search_fields = ['email_address','first_name','last_name']

class Searchable(admin.ModelAdmin):
    search_fields = ('user__email','user__first_name','user__last_name')

# Register your models here.
admin.site.register(AuthUser, CustomUserAdmin)
admin.site.register(Faculty,Searchable)
admin.site.register(Staff,Searchable)
admin.site.register(OCS,Searchable)
admin.site.register(ADPD,Searchable)
admin.site.register(ReferenceAccount,ReferenceAcc)