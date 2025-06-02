from django.contrib import admin
from .models import Car

class CarsAdmin(admin.ModelAdmin):
    model = Car
    list_display = ('id', 'car_model', 'engine_model', 'serial_number', 'manufacturer', 'release_date', 'car_image')
    list_display_links = ('id', 'car_model', 'serial_number')
    list_filter = ('engine_model', 'manufacturer')
    search_fields = ('serial_number', 'car_model', 'manufacturer')


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser

class CustomerUserAdmin(UserAdmin):
    model = CustomerUser
    list_display = ('email', 'username', 'first_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')  # можно добавить is_superuser и groups, если нужно
    search_fields = ('email', 'username',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'register_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(Car, CarsAdmin)
