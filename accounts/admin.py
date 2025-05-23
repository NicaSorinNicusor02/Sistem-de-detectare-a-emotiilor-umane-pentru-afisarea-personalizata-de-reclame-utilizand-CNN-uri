from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from .forms import CustomUserCreationForm, SHOPPING_CENTERS
from django import forms

class CustomUserChangeForm(UserChangeForm):
    city = forms.ChoiceField(choices=CustomUserCreationForm.CITY_CHOICES, required=False, label="Oraș")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.city:
            # seteaza valorile pentru shopping_center bazat pe orasul utilizatorului
            city = self.instance.city
            shopping_centers = SHOPPING_CENTERS.get(city, [])
            self.fields['shopping_center'] = forms.ChoiceField(
                choices=[('', 'Selectează centru comercial')] + shopping_centers,
                required=False,
                label="Centru comercial"
            )

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    fieldsets = (
        ("", {"fields": ("username", "password")}),
        ("Informații personale", {"fields": ("first_name", "last_name", "email", "city", "shopping_center", "store_name", "phone_number")}),
        ("Permisiuni", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Date importante", {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("username", "email", "display_city", "display_shopping_center", "store_name", "phone_number", "is_staff")
    search_fields = ("username", "email", "city", "shopping_center", "store_name", "phone_number")
    
    def display_city(self, obj):
        city_dict = dict(CustomUserCreationForm.CITY_CHOICES)
        return city_dict.get(obj.city, obj.city)
    display_city.short_description = 'Oraș'
    
    def display_shopping_center(self, obj):
        if obj.city and obj.shopping_center:
            centers = dict(SHOPPING_CENTERS.get(obj.city, []))
            return centers.get(obj.shopping_center, obj.shopping_center)
        return obj.shopping_center
    display_shopping_center.short_description = 'Centru comercial'


admin.site.register(CustomUser, CustomUserAdmin)