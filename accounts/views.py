import csv
import json
import time
from datetime import datetime

import cryptocode
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout ,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from social_core.exceptions import AuthException
from social_django import strategy

from ORB import settings
from utilities.emailer import send_email_asynch
from utilities.logger_util import Logger
from .forms import *
from UPM.models import *
from django.core.mail import EmailMessage


from bootstrap_modal_forms.generic import BSModalUpdateView,BSModalDeleteView
from django.core.paginator import Paginator


logger = Logger()


def loginPage(request):
    # update_users_to_default_perms()
    contact = Contact.objects.first()
    iserror = False
    error=''
    if request.user.is_authenticated:
        return redirect('indexPage')
    else:
        if request.method == 'POST':
            if(request.POST.get("action", "") == "guest"):
                return redirect('indexPage')
            
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                messages.success(request, "You are now logged in as " + str(user))
                logger.log_login(user)
                return redirect('indexPage')
            else:
                iserror = True
                error = "Wrong username or password."
        context = {"error":error,"iserror":iserror, "contact": contact}
        return render(request, 'accounts/login.html', context)
    

def logOutPage(request):
    logger.log_logout(request.user)
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
def viewProfile(request):
    user = request.user
    context = {'user':user}
    return render(request,'accounts/profile.html', context)

def editProfile(request):
    user= request.user
    form = EditUserForm(instance=user)

    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            logger.log_edit_own_profile(request.user, str(form.cleaned_data))
            form.save()
        return HttpResponseRedirect(reverse_lazy('profile'))

    context={'form':form}
    return render(request,'accounts/edit-profile.html',context)

@login_required(login_url='loginPage')
def AddUserPage(request):
    if not(request.user.is_superuser):
        return(redirect('viewBookings'))
    
    add = False #add new fields
    form = CreateUserForm()
    ut = 0
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        role = request.POST.get('role')

        #gets the role from the select tag in template
        if role == 'faculty':
            ut=1
        elif role == 'staff':
            ut=2
        elif role == 'ocs':
            ut=3
        elif role == 'adpd':
            ut=4
        else:
            ut=5

        #adds user to database if form is valid
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(False)
            user.user_type = ut

            data = form.cleaned_data
            dept_ID_CAMP = data.get("dp_CAMP")
            dept_ID_CAS = data.get("dp_CAS")
            # dept_ID_CN = data.get("dp_CN")
            dept_ID_CD = data.get("dp_CD")
            dept_ID_CP = data.get("dp_CP")
            dept_ID_CPH = data.get("dp_CPH")
            dept_ID_CM = data.get("dp_CM")
            col_ID = int(data.get("college"))

            if data.get("can_approve"):
                user.can_approve = True

            if data.get("can_remark"):
                user.can_remark = True

            if data.get("can_manage_equipment"):
                user.can_manage_equipment = True

            if data.get("can_manage_facilities"):
                user.can_manage_facilities = True

            if data.get("can_manage_terms"):
                user.can_manage_terms = True

            if data.get("can_upload_schedules"):
                user.can_upload_schedules = True

            if data.get("can_view_bookings"):
                user.can_view_bookings = True

            user.college = College.objects.get(id=col_ID)

            print(user.get_perms())

            if dept_ID_CAMP:
                if dept_ID_CAMP != "0":
                    user.department = Department.objects.get(id=dept_ID_CAMP)

            elif dept_ID_CAS:
                if dept_ID_CAS != "0":
                    user.department = Department.objects.get(id=dept_ID_CAS)

            # elif dept_ID_CN:
            #     if dept_ID_CN != "0":
            #         user.department = Department.objects.get(id=dept_ID_CN)

            elif dept_ID_CD:
                if dept_ID_CD != "0":
                    user.department = Department.objects.get(id=dept_ID_CD)

            elif dept_ID_CP:
                if dept_ID_CP != "0":
                    user.department = Department.objects.get(id=dept_ID_CP)

            elif dept_ID_CPH:
                if dept_ID_CPH != "0":
                    user.department = Department.objects.get(id=dept_ID_CPH)

            elif dept_ID_CM:
                if dept_ID_CM != "0":
                    user.department = Department.objects.get(id=dept_ID_CM)

            user.save()

            #adds user to their respective roles
            if ut == 1:
                Faculty.objects.create(user=user,college=user.college,dept=user.department,college_list = user.college.name)
            elif ut == 2:
                Staff.objects.create(user=user,college=user.college,dept=user.department)
            elif ut == 3:
                OCS.objects.create(user=user,college=user.college)
            elif ut == 4:
                ADPD.objects.create(user=user)
            elif ut == 5:
                AO.objects.create(user=user)

            user.save()
            print(user.get_perms())
            messages.success(request, "User '" + str(user) +"' has been added" )
            logger.log_create_user(request.user, user)
            return redirect('manageUsers')
        else:
            print(form.errors)

    context = {'form': form,'add':add,'ut':ut}


    return render(request,"accounts/add-user.html", context)

@login_required(login_url='loginPage')
def manageUsers(request):
    if not(request.user.is_superuser):
        return(redirect('viewBookings'))
    
    users = AuthUser.objects.filter(last_login__isnull=False).exclude(username='sysadmin')

    for user in users:
        if ReferenceAccount.objects.filter(email_address = user.email):
            setattr(user, 'isGoogle', 1)
        else:
            setattr(user, 'isGoogle', 0)

    if request.method =="POST":
        role = request.POST.get('role')
        if role == 'faculty':
            users = AuthUser.objects.filter(user_type=1)
        elif role == 'staff':
            users = AuthUser.objects.filter(user_type=2)
        elif role == 'ocs':
            users = AuthUser.objects.filter(user_type=3)
        elif role == 'adpd':
            users = AuthUser.objects.filter(user_type=4)
        elif role == 'ao':
            users = AuthUser.objects.filter(user_type=5)
    #Sets up Pagination
    try:
        records = request.GET['dropdown']
    except:
        records = 20

    p = Paginator(users, records)
    page = request.GET.get('page')
    usersPerPage = p.get_page(page)

    context={'users':usersPerPage,
             'records': records}
    
    return render(request,"accounts/users.html",context)

#update the table asynchronously
def users(request):
    data = dict()
    if request.method == 'GET':
        users = AuthUser.objects.filter(last_login__isnull=False).exclude(username='sysadmin')
        # users = AuthUser.objects.exclude(username='sysadmin')
        #Sets up Pagination
        try:
            records = request.GET['dropdown']
        except:
            records = 20
        p = Paginator(users, records)
        page = request.GET.get('page')
        usersPerPage = p.get_page(page)
        data['table'] = render_to_string(
            'accounts/user-table.html',
            {'users': usersPerPage},
            request=request
        )
        return JsonResponse(data)


# def completeLogin(request):
#     print("haha")
#     if not request.user.is_authenticated:
#         return redirect("loginPage")
#     # else:
#     try:
#         if request.user.is_active:
#             return redirect("viewBookings")
#         else:
#             return redirect("loginPage")
#     except Exception as e:
#         print(e)
#         return redirect("loginPage")

#edit user modal
def editUser(request,pk):
    user = AuthUser.objects.get(id=pk)
    if request.method == "POST":
        form= EditUserForm(request.POST, instance=user)

        if form.is_valid():
            logger.log_edit_profile(request.user, str(form.cleaned_data))
            form.save()

        return HttpResponseRedirect(reverse_lazy('manageUsers'))

    else:
        form = EditUserForm(instance=user)

        context = {'form': form,'u':user}
        return render(request, 'accounts/edit-user.html', context)

#change password modal
def changePass(request,pk):
    user = AuthUser.objects.get(id=pk)
    pw = PasswordChangeForm(user)
    if ReferenceAccount.objects.filter(email_address = user.email):
        isGoogle = 1
    else:
        isGoogle = 0

    if request.method == "POST":
        pw = PasswordChangeForm(data=request.POST, user=user)
        if pw.is_valid():
            pw.save()
            update_session_auth_hash(request, pw.user)
    context = {'pw': pw,'isGoogle': isGoogle}
    return render(request, 'accounts/change-password.html', context)

#delete user modal
class deleteUser(BSModalDeleteView):
    model = AuthUser
    template_name = 'accounts/delete-user.html'
    success_message = 'Success: User was deleted.'
    success_url = reverse_lazy('manageUsers')

    def post(self, request, *args, **kwargs):
        # Get the object being deleted
        self.object = self.get_object()

        # Call the delete method of the superclass to perform the actual deletion
        response = super().post(request, *args, **kwargs)

        # Add your custom logging logic here
        logger.log_delete_user(request.user, self.object)

        # Add a success message
        messages.success(self.request, self.success_message)

        return response


def importReferenceTable(request):
    if request.method == "POST":
        form = ReferenceTableCSVForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = None
            try:
                cleaned_data = form.clean_file()
            except ValidationError as e:
                messages.error(request, f"Validation Error: Only CSV Files are Allowed.", extra_tags='alert-danger')
                return redirect("/admin/accounts/referenceaccount/")
            decoded_file = cleaned_data.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            faculty_class = ["academic.", "academic.faculty"]
            active_status = ["active assignment"]

            for row in reader:
                id = row["HRIS_NUMBER"]
                ln = row["LASTNAME"]
                fn = row["FIRSTNAME"]
                mn = row["MIDDLENAME"]
                email = row["EMAIL_ADDRESS"]
                user_class = row["CLASS"]
                dept = row["DEPARTMENT"]
                college = row["COLLEGE"]
                status = row["STATUS"]
                dept_fk = None
                college_fk = None
                user_type = 0
                user_status = 0

                has_error = False

                try:
                    college_fk = College.objects.get(name__startswith=college)

                except Exception as e:
                    print("Unable to get College " + str(dept))
                    print(e)
                    has_error = True
                    messages.error(request, f"Invalid College: {college} ; for User: {ln}, {fn} {mn}, {email}", extra_tags='alert-danger')
                    continue

                if not (dept == college):
                    print(str(dept) + " vs " + str(college))
                    try:
                        dept_fk = Department.objects.get(name__startswith=dept)

                    except Exception as e:
                        print("Unable to get Department " + str(dept))
                        print(e)
                        has_error = True
                        messages.error(request, f"Invalid Department: {dept} ; for User: {ln}, {fn} {mn}, {email}", extra_tags='alert-danger')
                        continue


                if (str(user_class).lower() in faculty_class):
                    user_type = 1

                if (str(status).lower() in active_status):
                    user_status = 1

                if ("do not use" in str(ln).lower()):
                    has_error = True

                if not has_error:
                    ReferenceAccount.objects.create(
                        hris_number=id,
                        last_name=ln,
                        first_name=fn,
                        middle_name=mn,
                        email_address=email,
                        user_type=user_type,
                        department=dept_fk,
                        college=college_fk,
                        status=user_status
                    )
        return redirect("/admin/accounts/referenceaccount/")
    else:
        context = {
            'form':ReferenceTableCSVForm()
        }
        return render(request, 'admin/accounts/referenceaccount/csv_upload.html', context)

def failed_login(request):
    if request.user.is_authenticated:
        return redirect('viewBookings')
    if request.method == "POST":
        form = request_account(request.POST)
        if form.is_valid():
            print("Valid")
            print(type(form.cleaned_data.get("dp_CAS")))
            data = form.cleaned_data
            fn = data.get("first_name")
            mn = data.get("middle_name")
            ln = data.get("last_name")
            upmail = data.get("email_address")
            role_ID = int(data.get("user_type"))
            # dept_ID = int(data.get("department"))
            dept_ID_CAMP = data.get("dp_CAMP")
            dept_ID_CAS = data.get("dp_CAS")
            # dept_ID_CN = data.get("dp_CN")
            dept_ID_CD = data.get("dp_CD")
            dept_ID_CP = data.get("dp_CP")
            dept_ID_CPH = data.get("dp_CPH")
            dept_ID_CM = data.get("dp_CM")
            col_ID = int(data.get("college"))
            other = data.get("others")

            role = ""

            if role_ID == 1:
                role = "Faculty"
            elif role_ID == 2:
                role = "Staff"
            elif role_ID == 3:
                role = "OCS"
            elif role_ID == 4:
                role = "ADPD"
            elif role_ID == 5:
                role = "AO"
            else:
                role = "Invalid"

            col = ""

            if col_ID < 12:
                col = College.objects.get(id=col_ID).name
            elif col_ID == 12:
                col = "UPM Community Health Dev Program"
            elif col_ID == 13:
                col = "UPM National Institute For Health"
            elif col_ID == 14:
                col = "UPM Newborn Screening Ref Center"
            elif col_ID == 15:
                col = "UPM NTTC"
            elif col_ID == 16:
                col = "UPM Telehealth Center"
            else:
                col = "Others"

            dept = ""

            if dept_ID_CAMP:
                if dept_ID_CAMP != "0":
                    dept = Department.objects.get(id=dept_ID_CAMP).name

            elif dept_ID_CAS:
                if dept_ID_CAS != "0":
                    dept = Department.objects.get(id=dept_ID_CAS).name

            # elif dept_ID_CN:
            #     if dept_ID_CN != "0":
            #         dept = Department.objects.get(id=dept_ID_CN).name

            elif dept_ID_CD:
                if dept_ID_CD != "0":
                    dept = Department.objects.get(id=dept_ID_CD).name

            elif dept_ID_CP:
                if dept_ID_CP != "0":
                    dept = Department.objects.get(id=dept_ID_CP).name

            elif dept_ID_CPH:
                if dept_ID_CPH != "0":
                    dept = Department.objects.get(id=dept_ID_CPH).name

            elif dept_ID_CM:
                if dept_ID_CM != "0":
                    dept = Department.objects.get(id=dept_ID_CM).name

            sender = 'appsdev@post.upm.edu.ph'
            recipients = []
            recipients.append("pegasmen@up.edu.ph")
            # recipients.append("for.10dlsyes@gmail.com")
            subject = "[UPM ORBS] Account Request for [" + str(upmail) + "]"
            message_template = """
THIS IS AN AUTO GENERATED EMAIL

Dear Admin,

    Greetings!

    A user has submitted a request for an account on UPM ORBS. 
    
    The details of the request are as follows:
{user_details}

    Thank you for your attention to this matter.

Best regards,
UPM ORBS

(AUTOGENERATED: {time_now})
"""
            user_details = """        - First Name:\t    {fn}
        - Middle Name:\t {mn}
        - Last Name:\t   {ln}
        - UP Mail:\t      {up_mail}
        - User Type:\t    {user_type}"""
            user_details_str = ""
            if col_ID < 12:
                user_details += """
        - College:\t      {college}"""
                if dept:
                    user_details += """
        - Department:\t   {dept}"""

            else:
                if col == "Others":
                    user_details += """
        - College/Office:  {college} ({specified})"""
                else:
                    user_details += """
        - Office:\t        {college}"""

            user_details_str = user_details.format(
                fn=fn,
                mn=mn,
                ln=ln,
                up_mail=upmail,
                user_type=role,
                college=col,
                dept=dept,
                specified=other,
            )

            try:
                user = AuthUser.objects.get(email=upmail)
                if user:
                    if user.is_active:
                        messages.error(request, "You already have an Active Account, please Contact the Admin if you have trouble signing in")
                        context = {'form': form}
                        return render(request, 'accounts/failed_login.html', context)
                    else:
                        fn = user.first_name
                        ln = user.last_name
                        mn = "[Not Available (No Middle Name Field in DB)]"
                        upmail = user.email
                        role_ID = user.user_type
                        role = ""
                        if role_ID == 0:
                            role = "Admin"
                        elif role_ID == 1:
                            role = "Faculty"
                        elif role_ID == 2:
                            role = "Staff"
                        elif role_ID == 3:
                            role = "OCS"
                        elif role_ID == 4:
                            role = "ADPD"
                        elif role_ID == 5:
                            role = "AO"
                        else:
                            role = "Invalid"

                        col = ""
                        if user.college_id:
                            col = College.objects.get(id=user.college_id).name

                        if user.department_id:
                            dept = Department.objects.get(id=user.department_id).name

                        user_details_db = user_details.format(
                            fn=fn,
                            mn=mn,
                            ln=ln,
                            up_mail=upmail,
                            user_type=role,
                            college=col,
                            dept=dept,
                        )
                        user_details_str = "  USER IS ALREADY IN DATABASE BUT IS_ACTIVE IS 0 (OFF)\n" \
                                           "  To activate user, put a check on \"Is active\" checkbox on the user in Users table\n\n" \
                                           "    User Details on Database (Accounts -> Users table in Django Admin page):\n" + user_details_db + "\n\n" \
                                           "    Submitted Details:\n" + user_details_str
            except ObjectDoesNotExist:
                pass
            except Exception as e:
                print(e)

            message = message_template.format(
                user_details=user_details_str,
                time_now=datetime.now()
            )

            print(message)

            send_email_asynch(subject, message, sender, recipients)

            print("Success")
            messages.success(request, "Account Request Form Successfully Submitted")
            return redirect("roomView")
        else:
            print("Form has Error(s)")
            print(form.errors)
            messages.error(request, "Failed to Submit, please check the details you have entered.")
            # return redirect("failedLogin")
            context = {'form': form}
            return render(request, 'accounts/failed_login.html', context)
    else:
        context = {'form': request_account()}
        return render(request, 'accounts/failed_login.html', context)


def portal_seamless_auth(request):
    FAILED_REDIRECT_TO = "failedLogin"
    PORTAL_ERRORPAGE = "http://127.0.0.1:50000/upmportal_error"
    encrypted_data = request.GET.get('data', None)
    if not encrypted_data:
        return redirect("http://127.0.0.1:50000/no_enc_data")

    try:
        print(encrypted_data)
        decrypted_data = cryptocode.decrypt(encrypted_data.replace(" ", "+"), settings.SEAMLESS_KEY)
        print(decrypted_data)
        data = json.loads(decrypted_data)
        print(data)
        email = data.get('email', None)
        expire_in = data.get('expire_in', 0)
        timestamp = data.get('timestamp', 0)

        current_time = int(time.time())

        if current_time - timestamp > expire_in:
            return redirect("http://127.0.0.1:50000/expired_session")

    except Exception as e:
        print(e)
        return redirect("http://127.0.0.1:50000/" + str(e).replace(" ", "_"))

    if not email:
        return redirect("http://127.0.0.1:50000/no_email")

    try:
        user = AuthUser.objects.get(email=email)
        request.user = user
        if not (user.is_active):
            print("Not Active")
            user.is_active = False
            user.save()
            logout(request)
            return redirect(FAILED_REDIRECT_TO)
            # raise AuthFailed('You are not authorized to access this site.')
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("viewBookings")
    except AuthUser.DoesNotExist as e:
        print(e)

    try:
        ref = ReferenceAccount.objects.get(email_address=email)
        username = str(email).split("@")[0]
        AuthUser.objects.create(
            password=make_password(AuthUser.objects.make_random_password()),
            is_superuser=False,
            username=username,
            is_staff=False,
            is_active=ref.status,
            date_joined=datetime.now(),
            first_name=ref.first_name,
            last_name=ref.last_name,
            email=email,
            user_type=ref.user_type,
            college=ref.college,
            department=ref.department,
            can_remark=False,
            can_book=False,
            can_approve=False,
            can_manage_terms=False,
            can_view_bookings=False,
            can_manage_equipment=False,
            can_upload_schedules=False,
            can_manage_facilities=False,
        )
        user = AuthUser.objects.get(email=email)
        user_type = user.user_type
        if (user_type == 1):
            # Faculty
            Faculty.objects.create(user=user, college=ref.college, dept=ref.department,college_list = ref.college.name)
            user.appoint_permissions_faculty()
        elif (user_type == 2):
            # Staff
            Staff.objects.create(user=user, college=ref.college, dept=ref.department)
            user.appoint_permissions_staff()
        elif (user_type == 3):
            # OCS
            OCS.objects.create(user=user, college=ref.college)
            user.appoint_permissions_OCS()
        elif (user_type == 4):
            # ADPD
            ADPD.objects.create(user=user, college=ref.college)
            user.appoint_permissions_ADPD()
        elif (user_type == 5):
            # AO
            AO.objects.create(user=user, college=ref.college)
            user.appoint_permissions_AO()

        if (user.is_active):
            print("user activated")
            user.save()

        else:
            print("Ref - Not Active - but added in DB")
            user.is_active = False
            user.save()
            logout(request)
            return redirect(FAILED_REDIRECT_TO)

        print("reached end")
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("viewBookings")

    except ReferenceAccount.DoesNotExist as e:
        print("Does not Exist on Ref Acc")
        # raise AuthException('You are not authorized to access this site.')
        return redirect(FAILED_REDIRECT_TO)


def update_users_to_default_perms():
    all_users = AuthUser.objects.all()
    for user in all_users:
        user_type = user.user_type
        print(user_type)
        if user_type == 1:
            user.appoint_permissions_faculty()
        elif user_type == 2:
            user.appoint_permissions_staff()
        elif user_type == 3:
            user.appoint_permissions_OCS()
        elif user_type == 4:
            user.appoint_permissions_ADPD()
        elif user_type == 5:
            user.appoint_permissions_AO()
        user.save()