from cProfile import label
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelChoiceField, ModelForm,EmailField
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm, Textarea
import json
from django.core.exceptions import ValidationError
import re
from django.forms import ModelMultipleChoiceField
from .models import Room, Equipment


def is_valid_link(link):
    if not link:
        return True
    # Implement a regex check for a valid link
    link_pattern = re.compile(r'^https?://')
    return bool(link_pattern.match(link))

class AddTerm(ModelForm):
    date_start = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    date_end = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    class_start = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    class_end = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super(AddTerm, self).__init__(*args, **kwargs)
        self.fields['academicyear'].label = 'Academic Year (ex. "2019-2020")'
        self.fields['date_start'].label = 'Start Date'
        self.fields['date_end'].label = 'End Date'
        self.fields['class_start'].label = 'Start of Classes'
        self.fields['class_end'].label = 'End of Classes'

    class Meta:
        model = Term
        fields = ['academicyear','date_start','date_end','class_start','class_end','semester']

        labels={
            'academicyear':'Academic Year (ex. "2019-2020")',
            'date_start':'Starting Date',
            'date_end':'End Date',
            'class_start':'Start of Classes',
            'class_end':'End of Classes',
        }
        
class AddCollege(ModelForm):
    class Meta:
        model = College
        fields = ['name']

class AddBuild(ModelForm):
    class Meta:
        model = Building
        fields = ['name']

class AddDept(ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class AddEquipment(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'category']
        
    
    widgets = {
        'category': forms.Select(attrs={'class': 'custom-category-dropdown'}),
    }

    # Add choices for the category field
    CATEGORY_CHOICES = [
        ('Appliances and Devices', 'Appliances and Devices'),
        ('Furniture and Accessories', 'Furniture and Accessories'),
        ('Climate Control', 'Climate Control'),
        ('Laboratory Instruments', 'Laboratory Instruments'),
        ('Models and Microscopes', 'Models and Microscopes'),
        ('Balances and Scales', 'Balances and Scales'),
        ('Testing and Prep Equipment', 'Testing and Prep Equipment'),
        ('Physics Equipment', 'Physics Equipment'),
        ('Others', 'Others'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

class ManageEquipment(forms.ModelForm):
    equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Room
        fields = ['equipment']

    def grouped_choices(self):
        choices_by_category = {}
    
        for value, label in self.fields['equipment'].choices:
            equipment_name, category = label.split(" - ", 1)
            
            if category not in choices_by_category:
                choices_by_category[category] = []
                
            choices_by_category[category].append((value, equipment_name))
        
        choices = [(category, equipment_list) for category, equipment_list in choices_by_category.items()]
        return choices

    
#Add room form for the building view page
class AddRoom(ModelForm):
    class Meta:
        model = Room
        fields = ['name','capacity','room_type']

# class AddTermRoom(ModelForm):
#     class Meta:
#         model = Term
#         fields = ['room']

#Add Room form for the manage room page
class ColBuildForm(ModelForm):

    class Meta:
        model = Room
        fields = ('college','building','name','capacity','room_type')

class UploadForm(ModelForm):

    class Meta:
        model= ScheduleFile
        fields = ['term','file']

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        
        # Customize the queryset for the 'term' field to only include active terms
        self.fields['term'].queryset = Term.objects.filter(isActivated=True)

class EditEquipment(ModelForm):
    class Meta:
        model = Room
        fields = ['equipment']

#AO Edit Equipment

# class AOEditEquipment(ModelForm):
#     class Meta:
#         model = Room
#         fields = ['equipment']

# Add rooms from CSV for Django Admin's change room page
class RoomBulkUploadForm(forms.Form):
    csv_file = forms.FileField()

class EquipmentBulkUploadForm(forms.Form):
    csv_file = forms.FileField()


class AddScheduleExtra(ModelForm):
    class Meta:
        model = ScheduleExtra
        fields = ('modalName','additional_instructions','attachFile')
        widgets = {
            'additional_instructions': Textarea(attrs={'rows': 3, 'cols': 30,'class': 'row'}),  # Adjust rows and cols as needed
            'attachFile': Textarea(attrs={'rows': 2, 'cols': 30,'class': 'row','placeholder':"Attach your Google Drive Link here"}),  
        }

    def clean_attachFile(self):
        attachFile = self.cleaned_data.get('attachFile')

        # Perform a basic check for a valid link
        if not is_valid_link(attachFile):
            raise ValidationError("Invalid link. Please enter a Google Drive link or any valid link.")

        return attachFile
    # def __init__(self, *args, **kwargs):
    #     super(AddScheduleExtra, self).__init__(*args, **kwargs)
        
    #     # Modify the label for the attachFile field
    #     self.fields['attachFile'].label = 'Your Modified Label Text'

   