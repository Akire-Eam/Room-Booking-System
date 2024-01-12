from time import timezone
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from UPM.models import *



class AuthUser(AbstractUser):
    """creates user_types for all users"""
    FACULTY = 1
    STAFF = 2
    OCS = 3
    ADPD = 4
    AO = 5
    USER_TYPE_CHOICES = (
        (FACULTY, 'Faculty'),
        (STAFF, 'Staff'),
        (OCS, 'OCS'),
        (ADPD, 'ADPD'),
        (AO,'AO')
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, validators=[
        EmailValidator(allowlist=['up.edu.ph'])
    ])
    college = models.ForeignKey("UPM.College",on_delete=models.CASCADE,null=True,blank=True)
    department = models.ForeignKey("UPM.Department",on_delete=models.CASCADE,null=True,blank=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,null=True)

    is_active = models.BooleanField(default=True)

    # Flexible Permissions:
    # From Faculty and Staff:
    can_book = models.BooleanField(default=False, null=False, blank=False)

    # From ADPD (and v1.2.5 OCS):
    can_approve = models.BooleanField(default=False, null=False, blank=False)

    # From AO:
    can_remark = models.BooleanField(default=False, null=False, blank=False)
    can_manage_equipment = models.BooleanField(default=False, null=False, blank=False)
    # can_manage_rooms = models.BooleanField(default=False, null=False, blank=False)
    # can_manage_buildings = models.BooleanField(default=False, null=False, blank=False)
    # can_manage_colleges = models.BooleanField(default=False, null=False, blank=False)
    # These three are combined to:
    can_manage_facilities = models.BooleanField(default=False, null=False, blank=False)

    # From ADMIN:
    can_manage_terms = models.BooleanField(default=False, null=False, blank=False)

    # From OCS:
    can_upload_schedules = models.BooleanField(default=False, null=False, blank=False)

    # For every authenticated users:
    can_view_bookings = models.BooleanField(default=False, null=False, blank=False)


    def __str__(self):
        return self.username

    def getFullName(self):
        return self.first_name + ' ' + self.last_name + ' <' + self.email + '>'
    
    def getName(self):
        return self.first_name + ' ' + self.last_name

    def get_perms(self):
        output = [self.can_book, self.can_approve, self.can_remark, self.can_manage_equipment,
                  self.can_manage_facilities, self.can_manage_terms, self.can_upload_schedules, self.can_view_bookings]
        return output

    def appoint_permissions_faculty(self):
        self.can_view_bookings = True
        self.can_book = True

    def appoint_permissions_staff(self):
        self.can_view_bookings = True
        self.can_book = True

    def appoint_permissions_OCS(self):
        # self.can_view_bookings = True
        # self.can_approve = True
        self.can_upload_schedules = True

    def appoint_permissions_ADPD(self):
        self.can_view_bookings = True
        # self.can_approve = True

    def appoint_permissions_AO(self):
        self.can_approve = True
        self.can_view_bookings = True
        self.can_remark = True
        self.can_manage_facilities = True

    def can_not_book(self):
        return not self.can_book

    def can_not_approve(self):
        return not self.can_approve

    def can_not_remark(self):
        return not self.can_remark

    def can_not_manage_equipment(self):
        return not self.can_manage_equipment

    def can_not_manage_facilities(self):
        return not self.can_manage_facilities

    def can_not_manage_terms(self):
        return not self.can_manage_terms

    def can_not_upload_schedules(self):
        return not self.can_upload_schedules

    def can_not_view_bookings(self):
        return not self.can_view_bookings

    def remove_permissions(self):
        self.can_book = False
        self.can_approve = False
        self.can_remark = False
        self.can_manage_equipment = False
        self.can_manage_facilities = False
        self.can_manage_terms = False
        self.can_upload_schedules = False
        self.can_view_bookings = False


class Faculty(models.Model):
    user = models.OneToOneField(AuthUser,on_delete=models.CASCADE,null=True)
    college = models.ForeignKey("UPM.College",on_delete=models.CASCADE,null=True)
    dept = models.ForeignKey("UPM.Department",on_delete=models.CASCADE,null=True)
    college_list = models.CharField(max_length=200,null=True,blank=True)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        name = AuthUser.get_full_name(self.user)
        return name + ' <' + self.user.email + '>'
    
    
    def getName(self):
        return self.user.first_name + ' ' + self.user.last_name 


class OCS(models.Model):
    user = models.OneToOneField(AuthUser,on_delete=models.CASCADE,null=True)
    college = models.ForeignKey("UPM.College",on_delete=models.CASCADE,null=True)
    

    class Meta:
        verbose_name_plural = "College Secretaries"

    def __str__(self):
        name = AuthUser.get_full_name(self.user)
        return name + ' <' + self.user.email + '>'
    
    def getName(self):
        return self.user.first_name + ' ' + self.user.last_name 


class Staff(models.Model):
    user = models.OneToOneField(AuthUser,on_delete=models.CASCADE,null=True)

    college = models.ForeignKey("UPM.College",on_delete=models.CASCADE,null=True)
    dept = models.ForeignKey("UPM.Department",on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        name = AuthUser.get_full_name(self.user)
        return name + ' <' + self.user.email + '>'
    def getName(self):
        return self.user.first_name + ' ' + self.user.last_name 

class ADPD(models.Model):
    user = models.OneToOneField(AuthUser,on_delete=models.CASCADE,null=True)
    college = models.OneToOneField("UPM.College",on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name_plural = "ADPDs"

    def __str__(self):
        name = AuthUser.get_full_name(self.user)
        return name + ' <' + self.user.email + '>'
    def getName(self):
        return self.user.first_name + ' ' + self.user.last_name 

class AO(models.Model):
    user = models.OneToOneField(AuthUser,on_delete=models.CASCADE,null=True)
    college = models.OneToOneField("UPM.College",on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name_plural = "Administrative Officers"

    def __str__(self):
        name = AuthUser.get_full_name(self.user)
        return name + ' <' + self.user.email + '>'
    
    def getName(self):
        return self.user.first_name + ' ' + self.user.last_name 


class ReferenceAccount(models.Model):
    hris_number = models.IntegerField(blank=False, null=False)
    last_name = models.CharField(blank=False, null=False, max_length=50)
    first_name = models.CharField(blank=False, null=False, max_length=100)
    middle_name = models.CharField(blank=True, null=True, max_length=50)
    email_address = models.EmailField(blank=False, null=False)
    user_type = models.IntegerField(blank=False, null=False)
    department = models.ForeignKey("UPM.Department", on_delete=models.CASCADE, null=True, blank=True)
    college = models.ForeignKey("UPM.College", on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f'{self.id}: {self.last_name}, {self.first_name} {self.middle_name}' + ' <' + self.email_address + '>'