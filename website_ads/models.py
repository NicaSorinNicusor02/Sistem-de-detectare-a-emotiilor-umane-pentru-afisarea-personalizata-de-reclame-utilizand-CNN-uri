from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

class Ad(models.Model):
    CATEGORIES_CHOICES = [
        ('categorie1', 'Mancare și restaurante'),
        ('categorie2', 'Cinema, entertainment și cărți'),
        ('categorie3', 'Îmbrăcăminte, încălțăminte și accesorii vestimentare'),
        ('categorie4', 'Produse/Servicii pentru activități sportive'),
        ('categorie5', 'Tehnologie, gadgeturi, internet și telefonie'),
        ('categorie6', 'Jucării'),
        ('categorie7', 'Farmacii și plafare'),
        ('categorie8', 'Parfumuri și produse cosmetice'),
        ('categorie9', 'Cafenele'),
        ('categorie10', 'Supermarket'),
        ('categorie11', 'Agenții de turism')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # asociez reclama cu utilizatorul
    title = models.CharField(max_length=255, default="")  #adauga titlul reclamei
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ads/', null=True, blank=True)  # imaginea reclamei
    video = models.FileField(upload_to='ads_videos/', null=True, blank=True)  # adaugam campul video
    created_at = models.DateTimeField(auto_now_add=True)

    def get_category_display(self):
        """Returnează numele categoriei, nu codul (categorie1 -> Mancare)"""
        return dict(self.CATEGORIES_CHOICES).get(self.category, "Necunoscut")

User = get_user_model()

class Ticket(models.Model):
    STATUS_CHOICES = [
        ("open", "Deschis"),
        ("in_progress", "În lucru"),
        ("resolved", "Rezolvat"),
        ("closed", "Închis"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Nume utilizator")
    description = models.TextField(verbose_name="Descriere")  #descrierea tichetului
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    admin_response = models.TextField(blank=True, null=True, verbose_name="Răspuns administrator")  # raspunsul administratorului
    response_date = models.DateTimeField(blank=True, null=True, verbose_name="Data răspunsului")

    def __str__(self):
        return f"Tichet #{self.id} - {self.user.username} - {self.status}" 
    class Meta:
        verbose_name = "Tichet"
        verbose_name_plural = "Tichete"