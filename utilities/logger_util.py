from UPM.models import Term, College, Department, Building, Room,Schedule
from accounts.models import AuthUser
from logger.models import ActivityLog


class Logger:
    def log(self, action: str, log: str):
        ActivityLog.objects.create(action=action, log=log)

    def full_name(self, user: AuthUser):
        try:
            AuthUser.objects.get(id=user.id )
            user_fullname = user.getFullName()
        except AuthUser.DoesNotExist:
            user_fullname = "Guest"
        return user_fullname

    def log_login(self, user: AuthUser):
        log_str = (self.full_name(user) + " logged in.")
        self.log("Login", log_str)

    def log_login_from_portal(self, user: AuthUser):
        log_str = (self.full_name(user) + " logged in from UPM Portal.")
        self.log("Login from Portal", log_str)

    def log_login_GoogleSSO(self, user: AuthUser):
        log_str = (self.full_name(user) + " logged in via Google SSO.")
        self.log("Login via Google SSO", log_str)

    def log_logout(self, user: AuthUser):
        log_str = (self.full_name(user) + " logged out.")
        self.log("Logout", log_str)

    def log_edit_own_profile(self, user: AuthUser, form_data: str):
        log_str = (self.full_name(user) + " edited own profile. Form: " + form_data)
        self.log("Edit Profile", log_str)

    def log_create_user(self, user: AuthUser, user_added: AuthUser):
        log_str = (self.full_name(user) + " added User: " + self.full_name(user_added))
        self.log("Create User", log_str)

    def log_edit_profile(self, user: AuthUser, form_data: str):
        log_str = (self.full_name(user) + " edited another profile. Form: " + form_data)
        self.log("Edit Profile", log_str)

    def log_delete_user(self, deleter: AuthUser, deleted_user: AuthUser):
        log_str = (self.full_name(deleter) + " deleted User: " + self.full_name(deleted_user))
        self.log("Delete User", log_str)

    def log_remarks(self, remarker: AuthUser, remark: str, booking_str: str):
        log_str = (self.full_name(remarker) + " remarked: \"" + remark + "\" for Booking " + booking_str)
        self.log("Remarks", log_str)

    def log_edit_booking(self, user: AuthUser, booking_str: str, cleaned_data: str):
        log_str = (self.full_name(user) + " edited Booking " + booking_str + " Form: " + cleaned_data)
        self.log("Edit Booking", log_str)

    def log_rebook(self, user: AuthUser, booking_str: str, cleaned_data: str):
        log_str = (self.full_name(user) + " rebooked Booking " + booking_str + " Form: " + cleaned_data)
        self.log("Rebook", log_str)

    def log_approve_booking(self, user: AuthUser, booking_str: str):
        log_str = (self.full_name(user) + " approved Booking " + booking_str)
        self.log("Approve", log_str)

    def log_reject_booking(self, user: AuthUser, booking_str: str):
        log_str = (self.full_name(user) + " rejected Booking " + booking_str)
        self.log("Reject", log_str)

    def log_auto_reject_booking(self, booking_str: str):
        log_str = ("Auto-rejected Booking " + booking_str)
        self.log("Auto-Reject", log_str)

    def log_expire_booking(self, booking_str: str):
        log_str = ("Expired Booking " + booking_str)
        self.log("Expired", log_str)

    def log_upload_schedule_file(self, uploader: AuthUser, file_name: str):
        log_str = (self.full_name(uploader) + " uploaded the Schedule File: " + file_name)
        self.log("Upload Schedule", log_str)

    # newly added JC
    def log_remove_uploaded_schedule_file(self, deleter: AuthUser, file_name: str):
        log_str = (self.full_name(deleter) + " remove the Schedule File: " + file_name)
        self.log("Remove Schedule File", log_str)

    # newly added JC
    def log_add_or_modify_single_schedule_booking(self, modifier: AuthUser, modal_name: str):
        log_str = (self.full_name(modifier) + " remove the Selected Schedule Booking: " + modal_name)
        self.log("Modify Schedule Booking", log_str)

    # newly added JC
    def log_remove_single_schedule_booking(self,deleter: AuthUser, s_booking: Schedule,date_id: list = []):
        log_str = (self.full_name(deleter) + " remove the Selected Schedule Booking: " + str(s_booking) + (str(date_id) if date_id else " All Dates"))
        self.log("Remove Schedule Booking", log_str)

    def log_create_term(self, user: AuthUser, term_name: str):
        log_str = (self.full_name(user) + " created the Term: " + term_name)
        self.log("Create Term", log_str)

    def log_delete_term(self, user: AuthUser, term: Term):
        log_str = (self.full_name(user) + " deleted the Term: " + (str(term.semester) + " " + str(term.academicyear)) + "ID: " + str(term.id))
        self.log("Delete Term", log_str)
    
    #added jc
    def log_switch_term(self, user: AuthUser, term: Term, isactivate):
        log_str = (self.full_name(user) + f" {isactivate} the Term: " + (str(term.semester) + " " + str(term.academicyear)) + "ID: " + str(term.id))
        self.log(f"{isactivate} Term", log_str)

    def log_create_college(self, user: AuthUser, college_name: str):
        log_str = (self.full_name(user) + " created the College: " + college_name)
        self.log("Create College", log_str)

    def log_delete_college(self, user: AuthUser, college: College):
        log_str = (self.full_name(user) + " deleted the College: " + (str(college.name)) + "ID: " + str(college.id))
        self.log("Delete College", log_str)

    def log_create_equipment(self, user: AuthUser, equipment_name: str):
        log_str = (self.full_name(user) + " created the Equipment: " + equipment_name)
        self.log("Create Equipment", log_str)

    def log_edit_equipment(self, user: AuthUser, form_data: str):
        log_str = (self.full_name(user) + " edited an Equipment. Form: " + form_data)
        self.log("Edit Equipment", log_str)

    def log_create_dept(self, user: AuthUser, dept: Department):
        log_str = (self.full_name(user) + " created the Department: " + dept.name + " for College: " + str(dept.college.name))
        self.log("Create Department", log_str)

    def log_delete_dept(self, user: AuthUser, dept: Department):
        log_str = (self.full_name(user) + " deleted the Department: " + dept.name + " for College: " + str(dept.college.name))
        self.log("Delete Department", log_str)

    def log_create_building(self, user: AuthUser, building: Building):
        log_str = (self.full_name(user) + " created the Building: " + building.name + " for College: " + str(building.college.name))
        self.log("Create Building", log_str)

    def log_delete_building(self, user: AuthUser, building: Building):
        log_str = (self.full_name(user) + " deleted the Building: " + building.name + " for College: " + str(building.college.name))
        self.log("Delete Building", log_str)

    def log_create_room(self, user: AuthUser, room: Room):
        log_str = (self.full_name(user) + " created the Room: " + room.name + "for Building: " + str(room.building.name) + " for College: " + str(room.college.name))
        self.log("Create Room", log_str)

    def log_delete_room(self, user: AuthUser, room: Room):
        log_str = (self.full_name(user) + " deleted the Room: " + room.name + "for Building: " + str(room.building.name) + " for College: " + str(room.college.name))
        self.log("Delete Room", log_str)
    # added jc
    def log_hide_o_activate_room(self, user: AuthUser, room: Room):
        log_str = (self.full_name(user) + ("Activate" if room.isActivated else "Hide") + room.name + "for Building: " + str(room.building.name) + " for College: " + str(room.college.name))
        self.log("Activate Room" if room.isActivated else "Hide Room", log_str)

    def log_edit_room(self, user: AuthUser, form_data: str):
        log_str = (self.full_name(user) + " edited a Room. Form: " + form_data)
        self.log("Edit Room", log_str)

    def log_upload_room_file(self, uploader: AuthUser, file_name: str):
        log_str = (self.full_name(uploader) + " uploaded the Room File: " + file_name)
        self.log("Upload Room", log_str)

    def log_upload_equipment_file(self, uploader: AuthUser, file_name: str):
        log_str = (self.full_name(uploader) + " uploaded the Equipment File: " + file_name)
        self.log("Upload Equipment", log_str)

    def log_create_booking(self, user: AuthUser, booking_str: str):
        log_str = (self.full_name(user) + " created Booking " + booking_str)
        self.log("Create Booking", log_str)

    def log_delete_booking(self, user: AuthUser, booking_str: str):
        log_str = (self.full_name(user) + " deleted Booking " + booking_str)
        self.log("Delete Booking", log_str)

    def log_download_approved_bookings_csv(self, downloader: AuthUser, file_name: str):
        try:
            log_str = (self.full_name(downloader) + " downloaded the Approved Booking CSV File: " + file_name + " for College: " + str(downloader.college.name))
        except AttributeError:
            log_str = (self.full_name(downloader) + " downloaded the Approved Booking CSV File: " + file_name)
        self.log("Download ApprovedBooking", log_str)

