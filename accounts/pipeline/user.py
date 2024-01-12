from django.contrib import messages, auth
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from social_core.exceptions import AuthException, AuthFailed

from accounts.models import *
from UPM.models import *
from UPM.urls import *
from utilities.logger_util import Logger



def user_details(backend, strategy, details, response, user=None, *args, **kwargs):
    return {'details': dict(response, **details)}

def check_user(backend, strategy, details, response, user=None, *args, **kwargs):
    FAILED_REDIRECT_TO = "failedLogin"
    try: 
        AuthUser.objects.get(email=response['email'])
    except:
        
        try:
            print(response['email'])
            ref = ReferenceAccount.objects.get(email_address=response['email'])
            print(ref)
            user = AuthUser(
                    email=ref.email_address,
                    username = ref.email_address.split("@")[0],
                    user_type = ref.user_type,
                    first_name=ref.first_name,
                    last_name=ref.last_name,
                    college = ref.college,
                    department = ref.department,
                )
            
            user.save()
            
            if (ref.user_type == 1):
                # Faculty
                Faculty.objects.create(user=user, college=ref.college, dept=ref.department,college_list = ref.college.name)
                user.appoint_permissions_faculty()
            elif (ref.user_type == 2):
                # Staff
                Staff.objects.create(user=user, college=ref.college, dept=ref.department)
                user.appoint_permissions_staff()
            elif (ref.user_type == 3):
                # OCS
                OCS.objects.create(user=user, college=ref.college)
                user.appoint_permissions_OCS()
            elif (ref.user_type == 4):
                # ADPD
                ADPD.objects.create(user=user, college=ref.college)
                user.appoint_permissions_ADPD()
            elif (ref.user_type == 5):
                # AO
                AO.objects.create(user=user, college=ref.college)
                user.appoint_permissions_AO()

            user.save()

        except Exception as e:
                print(e)
                # if user does not exist in ReferenceAccount
                return redirect(FAILED_REDIRECT_TO)
    
    return {'uid': AuthUser.objects.get(email=response['email']).id}

            


def create_faculty(backend, strategy, details, response, user=None, *args, **kwargs):
    FAILED_REDIRECT_TO = "failedLogin"
    try:
        if (user.user_type is None) and (not user.is_superuser):
            # if user does not have faculty account yet, create one
            try:
                ref = ReferenceAccount.objects.get(email_address=user.email)
                print("Exists on Ref")
                print(ref)
                user_type = ref.user_type
                print(str(user_type) + ": " + str(type(user_type)))
                user.user_type = user_type
                print(user)
                user.password = make_password(AuthUser.objects.make_random_password())
                print(user.password)
                user.college = ref.college
                print(user.college)
                user.department = ref.department
                print(user.department)
                user.is_active = ref.status
                print("user was saved")
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
                    auth.logout(strategy.request)
                    return redirect(FAILED_REDIRECT_TO)
                print("reached end")
            except ReferenceAccount.DoesNotExist:
                print("Does not Exist on Ref Acc")
                raise AuthException(strategy.backend, 'You are not authorized to access this site.')
        else:
            if not (user.is_active):
                print("Not Active")
                user.is_active = False
                user.save()
                auth.logout(strategy.request)
                return redirect(FAILED_REDIRECT_TO)
                # raise AuthFailed('You are not authorized to access this site.')
            print("User exists on DB")
            logger = Logger()
            logger.log_login_GoogleSSO(user)
            # User will be redirected to "/"
    except Exception as e:
        print("Not Active")
        print(e)
        print("Exception")
        user.is_active = False
        user.save()
        auth.logout(strategy.request)
        return redirect(FAILED_REDIRECT_TO)
        # raise AuthFailed('You are not authorized to access this site.')