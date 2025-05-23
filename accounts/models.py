from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property

class CustomUser(AbstractUser):
    city = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name="Prenume")
    last_name = models.CharField(max_length=50, verbose_name="Nume")
    store_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nume magazin") 
    shopping_center = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, verbose_name="Număr telefon")
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username
    
    @cached_property
    def get_city_display(self):
        from .forms import CustomUserCreationForm
        city_dict = dict(CustomUserCreationForm.CITY_CHOICES)
        return city_dict.get(self.city, self.city)
        
    @cached_property
    def get_shopping_center_display(self):
        from .forms import SHOPPING_CENTERS
        if self.city and self.shopping_center:
            centers = dict(SHOPPING_CENTERS.get(self.city, []))
            return centers.get(self.shopping_center, self.shopping_center)
        return self.shopping_center
