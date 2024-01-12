from django import forms
import django_filters
from django_select2.forms import Select2MultipleWidget
from django.db.models import Q
from bookingapp.models import *
import json

from .models import *


#Filtering the rooms
class RoomFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        method='filter_name',
        widget=forms.TextInput(attrs={'class': 'custom-field-class', 'data-placeholder': 'Search rooms'}),
    )
    college = django_filters.ModelMultipleChoiceFilter(
        queryset=College.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'custom-field-class', 'data-placeholder': 'Select colleges'}),
        method='filter_college'
    )
    building = django_filters.ModelMultipleChoiceFilter(
        queryset=Building.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'custom-field-class', 'data-placeholder': 'Select buildings'}),
        method='filter_building'
    )
    room_type = django_filters.ModelMultipleChoiceFilter(
        queryset=RoomType.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'custom-field-class', 'data-placeholder': 'Select room types'}),
        method='filter_room_type'
    )
    capacity = django_filters.RangeFilter(
        field_name='capacity',
        method='filter_capacity'
    )
    equipment = django_filters.ModelMultipleChoiceFilter(
        queryset=Equipment.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'custom-field-class', 'data-placeholder': 'Select equipments'}),
        method='filter_equipment'
    )

    def __init__(self, *args, **kwargs):
        super(RoomFilter, self).__init__(*args, **kwargs)
        self.filters['name'].label = "Room Name"
        

    class Meta:
        model = Room
        fields = ('name','college','building','room_type','capacity','equipment')

    def filter_name(self, queryset, name, value):
        # # Sanitize the value to prevent SQL injection
        # sanitized_value = value.lower().replace(' ', '')

        # # Construct the SQL query with sanitized value using the LIKE operator
        # where_clause = "LOWER(REPLACE(name, ' ', '')) LIKE '%{0}%'".format(sanitized_value)

        # # Filter the queryset using the constructed SQL query
        # queryset = queryset.extra(where=[where_clause])

        if queryset.model is Room:
            queryset = queryset.filter(Q(name__icontains=value) | Q(name=value))
        elif queryset.model in [Booking, Schedule]:
            queryset = queryset.filter(Q(room__name__icontains=value) | Q(room__name=value))

        return queryset
    
    def filter_college(self, queryset, name, value):
        college_query = Q()
        for college in value:
            if queryset.model is Room:
                college_query |= Q(college=college)
            elif queryset.model in [Booking, Schedule]:
                college_query |= Q(room__college=college)
        
        return queryset.filter(college_query).distinct()
    
    def filter_building(self, queryset, name, value):
        building_query = Q()
        for building in value:
            if queryset.model is Room:
                building_query |= Q(building=building)
            elif queryset.model in [Booking, Schedule]:
                building_query |= Q(room__building=building)
        
        return queryset.filter(building_query).distinct()
    
    def filter_room_type(self, queryset, name, value):
        room_type_query = Q()
        for room_type in value:
            if queryset.model is Room:
                room_type_query |= Q(room_type=room_type)
            elif queryset.model in [Booking, Schedule]:
                room_type_query |= Q(room__room_type=room_type)
        
        return queryset.filter(room_type_query).distinct()
    
    def filter_capacity(self, queryset, name, value):
        # Convert the slice object to a tuple
        min_capacity, max_capacity = value.start, value.stop

        if queryset.model is Room:
            if min_capacity is not None:
                queryset = queryset.filter(capacity__gte=min_capacity)
            if max_capacity is not None:
                queryset = queryset.filter(capacity__lte=max_capacity)
        elif queryset.model in [Booking, Schedule]:
            if min_capacity is not None:
                queryset = queryset.filter(room__capacity__gte=min_capacity)
            if max_capacity is not None:
                queryset = queryset.filter(room__capacity__lte=max_capacity)
        
        return queryset

    def filter_equipment(self, queryset, name, value):
        # Filter the queryset to include only objects that have all selected equipment
        for equipment in value:
            if queryset.model is Room:
                queryset = queryset.filter(equipment=equipment)
            elif queryset.model in [Booking, Schedule]:
                queryset = queryset.filter(room__equipment=equipment)
        
        return queryset.distinct()
    
class ScheduleFilter(django_filters.FilterSet):
    input = []
    subject = django_filters.CharFilter(
        field_name='subject',
        method='filter_subject'
    )

    def __init__(self, *args, **kwargs):
        super(ScheduleFilter, self).__init__(*args, **kwargs)
        self.filters['subject'].label = "Subject"

    class Meta:
        model = Schedule
        fields = ['subject']

    def filter_subject(self, queryset, name, value):
        # Filter the queryset to include objects that match the provided name
        # or objects that have names containing the provided value
        if queryset.model is Room:
            queryset = queryset.filter(Q(schedule__subject__icontains=value) | Q(schedule__subject=value) | 
                                       Q(booking__subject__icontains=value) | Q(booking__subject=value))
        elif queryset.model is Booking:
            queryset = queryset.filter((Q(subject__icontains=value) | Q(subject=value)) & Q(status = Status.APPROVED))
        elif queryset.model is Schedule:
            queryset = queryset.filter(Q(subject__icontains=value) | Q(subject=value))
        
        return queryset.distinct()