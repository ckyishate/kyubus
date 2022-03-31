from django.contrib import admin
from django.contrib.auth.models import Group
from . models import Bus, Routes, Booking, Payment, Feedback
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms  import UserAdminCreationForm, UserAdminChangeForm

# removegroup model from admin
admin.site.unregister(Group)




User = get_user_model()
class UserAdmin(admin.ModelAdmin):
    search_fields=['email']
    list_display =['first_Name', 'last_Name', 'email','sex', 'contact','admin']

    class Meta:
        model=User


admin.site.register(User, UserAdmin)




class BusAdmin(admin.ModelAdmin):
    list_display =['name','plate_number','no_of_seats','driver_attached','mech_status']

admin.site.register(Bus, BusAdmin)



class RoutesAdmin(admin.ModelAdmin):
    list_display =['source','destination','date','departure','fare','bSeats','bus']
    search_fields=['source','date','departure']
admin.site.register(Routes, RoutesAdmin)



class BookingAdmin(admin.ModelAdmin):
    list_display =['user','date','seat','route']

admin.site.register(Booking, BookingAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = [ 'user','payment_method','time_stamp']

admin.site.register(Payment, PaymentAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'timestamp', 'reply']
admin.site.register(Feedback, FeedbackAdmin)

