from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelChoiceField, ModelForm,EmailField
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *

from bootstrap_modal_forms.forms import PopRequestMixin,CreateUpdateAjaxMixin

class CreateUserForm(UserCreationForm):
    college_choices = (
        ("", "Choose"),
        ("1", "College of Allied Medical Professions"),
        ("2", "College of Arts and Sciences"),
        ("4", "College of Dentistry"),
        ("5", "College of Nursing"),
        ("6", "College of Pharmacy"),
        ("10", "College of Public Health"),
        ("11", "College of Medicine"),
        ("12", "UPM Community Health Dev Program"),
        ("13", "UPM National Institute For Health"),
        ("14", "UPM Newborn Screening Ref Center"),
        ("15", "UPM NTTC"),
        ("16", "UPM Telehealth Center"),
        ("17", "Others"),
    )

    dept_choices_CAMP = (
        ("", "Choose"),
        ("0", "No Department"),
        ("8", "Department of Occupational Therapy"),
        ("9", "Department of Physical Therapy"),
        ("10", "Department of Speech Pathology"),
    )

    dept_choices_CAS = (
        ("", "Choose"),
        ("0", "No Department"),
        ("2", "Department of Arts and Communication (DAC)"),
        ("3", "Department of Behavioral Sciences (DBS)"),
        ("4", "Department of Biology (DB)"),
        ("5", "Department of Physical Education (DPE)"),
        ("6", "Department of Physical Sciences and Mathematics (DPSM)"),
        ("7", "Department of Social Sciences (DSS)"),
    )

    dept_choices_CD = (
        ("", "Choose"),
        ("0", "No Department"),
        ("11", "Department of Clinical Dental Health Sciences"),
        ("12", "Department of Community Dentistry"),
        ("13", "Department of Basic Dental Health Sciences"),
    )

    # dept_choices_CN = (
    #     ("", "Choose"),
    # )

    dept_choices_CP = (
        ("", "Choose"),
        ("0", "No Department"),
        ("35", "Department of Pharmacy"),
        ("36", "Department of Industrial Pharmacy"),
        ("37", "Department of Pharmaceutical Chemistry"),
    )

    dept_choices_CPH = (
        ("", "Choose"),
        ("0", "No Department"),
        ("43", "Department of Epidemiology and Biostatistics"),
        ("44", "Department of Medical Microbiology"),
        ("45", "Department of Parasitology"),
        ("46", "Department of Health Policy and Administration"),
        ("47", "Department of Environmental and Occupational Health"),
        ("48", "Department of Nutrition"),
        ("49", "Department of Health Promotion and Education"),
    )

    dept_choices_CM = (
        ("", "Choose"),
        ("0", "No Department"),
        ("14", "Department of Pediatrics"),
        ("15", "Department of Medicine"),
        ("16", "Department of Surgery"),
        ("17", "Department of Anatomy"),
        ("18", "Department of Pathology"),
        ("19", "Department of Otorhinolaryngology"),
        ("20", "Department of Rehabilitation Medicine"),
        ("21", "Department of Radiology"),
        ("22", "Department of Obstetrics and Gynecology"),
        ("23", "Department of Ophthalmology and Visual Sciences"),
        ("24", "Department of Clinical Epidemiology"),
        ("25", "Department of Family and Community Medicine"),
        ("26", "Department of Orthopedics"),
        ("27", "Department of Physiology"),
        ("28", "Department of Psychiatry and Behavioral Medicine"),
        ("29", "Department of Neurosciences"),
        ("30", "Department of Anesthesiology"),
        ("31", "Department of Dermatology"),
        ("32", "Department of Pharmacology and Toxicology"),
        ("33", "Department of Biochemistry and Molecular Biology"),
        ("34", "Department of Emergency Medicine"),
    )


    last_name = forms.CharField(required=True, max_length=50)
    first_name = forms.CharField(required=True, max_length=100)
    middle_name = forms.CharField(required=False, max_length=50)
    email = forms.EmailField(required=True)
    dp_CAMP = forms.ChoiceField(choices=dept_choices_CAMP, required=False)
    dp_CAS = forms.ChoiceField(choices=dept_choices_CAS, required=False)
    dp_CD = forms.ChoiceField(choices=dept_choices_CD, required=False)
    # dp_CN = forms.ChoiceField(choices=dept_choices_CN, required=False)
    dp_CP = forms.ChoiceField(choices=dept_choices_CP, required=False)
    dp_CPH = forms.ChoiceField(choices=dept_choices_CPH, required=False)
    dp_CM = forms.ChoiceField(choices=dept_choices_CM, required=False)
    college = forms.ChoiceField(choices=college_choices, required=True)
    default_permissions = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = "Last Name"
        self.fields['first_name'].label = "First Name"
        self.fields['middle_name'].label = "Middle Name"
        self.fields['college'].label = "Select College/Office"
        self.fields['dp_CAMP'].label = "Select Department"
        self.fields['dp_CAS'].label = "Select Department"
        self.fields['dp_CD'].label = "Select Department"
        # self.fields['dp_CN'].label = "Select Department"
        self.fields['dp_CP'].label = "Select Department"
        self.fields['dp_CPH'].label = "Select Department"
        self.fields['dp_CM'].label = "Select Department"

    #only allow @up.edu.ph emails
    def clean_email(self):
        data = self.cleaned_data['email']
        if "@up.edu.ph" not in data:   # any check you need
            raise forms.ValidationError("Must be a UP email address (up.edu.ph)")
        return data

    class Meta:
        model = AuthUser
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2',
                  'can_book', 'can_approve', 'can_remark', 'can_manage_equipment', 'can_manage_facilities',
                  'can_manage_terms', 'can_upload_schedules', 'can_view_bookings']

class EditUserForm(UserChangeForm):

    class Meta:
        model= AuthUser
        fields = ['first_name','last_name','username','password','college','department']


class ReferenceTableCSVForm(forms.Form):
    csv = forms.FileField()
    def clean_file(self):
        data = self.cleaned_data['csv']
        file_name = str(data.name)
        if file_name.endswith(".csv"):
            content_type = data.content_type
            if content_type == "text/csv":
                return data
            else:
                raise ValidationError(_("Invalid Content Type. Only CSV files are allowed."))
        else:
            raise ValidationError(_("Invalid Content Type. Only CSV files are allowed."))


class request_account(forms.Form):
    college_choices = (
        ("", "Choose"),
        ("1", "College of Allied Medical Professions"),
        ("2", "College of Arts and Sciences"),
        ("4", "College of Dentistry"),
        ("5", "College of Nursing"),
        ("6", "College of Pharmacy"),
        ("10", "College of Public Health"),
        ("11", "College of Medicine"),
        ("12", "UPM Community Health Dev Program"),
        ("13", "UPM National Institute For Health"),
        ("14", "UPM Newborn Screening Ref Center"),
        ("15", "UPM NTTC"),
        ("16", "UPM Telehealth Center"),
        ("17", "Others"),
    )

    dept_choices = (
        ("", "Choose"),
        ("8", "Department of Occupational Therapy"),
        ("9", "Department of Physical Therapy"),
        ("10", "Department of Speech Pathology"),
        ("2", "Department of Arts and Communication (DAC)"),
        ("3", "Department of Behavioral Sciences (DBS)"),
        ("4", "Department of Biology (DB)"),
        ("5", "Department of Physical Education (DPE)"),
        ("6", "Department of Physical Sciences and Mathematics (DPSM)"),
        ("7", "Department of Social Sciences (DSS)"),
        ("11", "Department of Clinical Dental Health Sciences"),
        ("12", "Department of Community Dentistry"),
        ("13", "Department of Basic Dental Health Sciences"),
        ("35", "Department of Pharmacy"),
        ("36", "Department of Industrial Pharmacy"),
        ("37", "Department of Pharmaceutical Chemistry"),
        ("43", "Department of Epidemiology and Biostatistics"),
        ("44", "Department of Medical Microbiology"),
        ("45", "Department of Parasitology"),
        ("46", "Department of Health Policy and Administration"),
        ("47", "Department of Environmental and Occupational Health"),
        ("48", "Department of Nutrition"),
        ("49", "Department of Health Promotion and Education"),
        ("14", "Department of Pediatrics"),
        ("15", "Department of Medicine"),
        ("16", "Department of Surgery"),
        ("17", "Department of Anatomy"),
        ("18", "Department of Pathology"),
        ("19", "Department of Otorhinolaryngology"),
        ("20", "Department of Rehabilitation Medicine"),
        ("21", "Department of Radiology"),
        ("22", "Department of Obstetrics and Gynecology"),
        ("23", "Department of Ophthalmology and Visual Sciences"),
        ("24", "Department of Clinical Epidemiology"),
        ("25", "Department of Family and Community Medicine"),
        ("26", "Department of Orthopedics"),
        ("27", "Department of Physiology"),
        ("28", "Department of Psychiatry and Behavioral Medicine"),
        ("29", "Department of Neurosciences"),
        ("30", "Department of Anesthesiology"),
        ("31", "Department of Dermatology"),
        ("32", "Department of Pharmacology and Toxicology"),
        ("33", "Department of Biochemistry and Molecular Biology"),
        ("34", "Department of Emergency Medicine"),
    )

    dept_choices_CAMP = (
        ("", "Choose"),
        ("0", "No Department"),
        ("8", "Department of Occupational Therapy"),
        ("9", "Department of Physical Therapy"),
        ("10", "Department of Speech Pathology"),
    )

    dept_choices_CAS = (
        ("", "Choose"),
        ("0", "No Department"),
        ("2", "Department of Arts and Communication (DAC)"),
        ("3", "Department of Behavioral Sciences (DBS)"),
        ("4", "Department of Biology (DB)"),
        ("5", "Department of Physical Education (DPE)"),
        ("6", "Department of Physical Sciences and Mathematics (DPSM)"),
        ("7", "Department of Social Sciences (DSS)"),
    )

    dept_choices_CD = (
        ("", "Choose"),
        ("0", "No Department"),
        ("11", "Department of Clinical Dental Health Sciences"),
        ("12", "Department of Community Dentistry"),
        ("13", "Department of Basic Dental Health Sciences"),
    )

    # dept_choices_CN = (
    #     ("", "Choose"),
    # )

    dept_choices_CP = (
        ("", "Choose"),
        ("0", "No Department"),
        ("35", "Department of Pharmacy"),
        ("36", "Department of Industrial Pharmacy"),
        ("37", "Department of Pharmaceutical Chemistry"),
    )

    dept_choices_CPH = (
        ("", "Choose"),
        ("0", "No Department"),
        ("43", "Department of Epidemiology and Biostatistics"),
        ("44", "Department of Medical Microbiology"),
        ("45", "Department of Parasitology"),
        ("46", "Department of Health Policy and Administration"),
        ("47", "Department of Environmental and Occupational Health"),
        ("48", "Department of Nutrition"),
        ("49", "Department of Health Promotion and Education"),
    )

    dept_choices_CM = (
        ("", "Choose"),
        ("0", "No Department"),
        ("14", "Department of Pediatrics"),
        ("15", "Department of Medicine"),
        ("16", "Department of Surgery"),
        ("17", "Department of Anatomy"),
        ("18", "Department of Pathology"),
        ("19", "Department of Otorhinolaryngology"),
        ("20", "Department of Rehabilitation Medicine"),
        ("21", "Department of Radiology"),
        ("22", "Department of Obstetrics and Gynecology"),
        ("23", "Department of Ophthalmology and Visual Sciences"),
        ("24", "Department of Clinical Epidemiology"),
        ("25", "Department of Family and Community Medicine"),
        ("26", "Department of Orthopedics"),
        ("27", "Department of Physiology"),
        ("28", "Department of Psychiatry and Behavioral Medicine"),
        ("29", "Department of Neurosciences"),
        ("30", "Department of Anesthesiology"),
        ("31", "Department of Dermatology"),
        ("32", "Department of Pharmacology and Toxicology"),
        ("33", "Department of Biochemistry and Molecular Biology"),
        ("34", "Department of Emergency Medicine"),
    )

    user_type_choices = (
        ("", "Choose"),
        ("1", "Faculty"),
        ("2", "Staff"),
        ("3", "College Secretary"),
        ("4", "ADPD"),
        ("5", "AO"),
    )

    last_name = forms.CharField(required=True, max_length=50)
    first_name = forms.CharField(required=True, max_length=100)
    middle_name = forms.CharField(required=False, max_length=50)
    email_address = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=user_type_choices, required=True)
    department = forms.ChoiceField(choices=dept_choices, required=False)
    dp_CAMP = forms.ChoiceField(choices=dept_choices_CAMP, required=False)
    dp_CAS = forms.ChoiceField(choices=dept_choices_CAS, required=False)
    dp_CD = forms.ChoiceField(choices=dept_choices_CD, required=False)
    # dp_CN = forms.ChoiceField(choices=dept_choices_CN, required=False)
    dp_CP = forms.ChoiceField(choices=dept_choices_CP, required=False)
    dp_CPH = forms.ChoiceField(choices=dept_choices_CPH, required=False)
    dp_CM = forms.ChoiceField(choices=dept_choices_CM, required=False)
    college = forms.ChoiceField(choices=college_choices, required=True)
    others = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(request_account, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = "Last Name"
        self.fields['first_name'].label = "First Name"
        self.fields['middle_name'].label = "Middle Name"
        self.fields['email_address'].label = "UP Mail (@up.edu.ph)"
        self.fields['user_type'].label = "Select Role"
        self.fields['college'].label = "Select College/Office"
        self.fields['dp_CAMP'].label = "Select Department"
        self.fields['dp_CAS'].label = "Select Department"
        self.fields['dp_CD'].label = "Select Department"
       # self.fields['dp_CN'].label = "Select Department"
        self.fields['dp_CP'].label = "Select Department"
        self.fields['dp_CPH'].label = "Select Department"
        self.fields['dp_CM'].label = "Select Department"
        self.fields['others'].label = 'Please Specify'

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        data = self.cleaned_data.get('email_address')
        if data:
            if "@up.edu.ph" not in data:   # any check you need
                raise forms.ValidationError("Must be a UP email address (up.edu.ph)")
            return cleaned_data
        else:
            raise forms.ValidationError("Must be a UP email address (up.edu.ph)")
