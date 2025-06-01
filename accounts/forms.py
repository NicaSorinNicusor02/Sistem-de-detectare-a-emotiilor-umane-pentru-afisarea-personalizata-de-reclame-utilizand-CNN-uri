from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


SHOPPING_CENTERS = {
    'bucurestisector1': [('promenada_mall', 'Promenada Mall'),
                         ('baneasa_shopping_city', 'Baneasa Shopping City')],

    'bucurestisector2': [('mega_mall', 'Mega Mall'),
                         ('veranda_mall', 'Veranda Mall')],

    'bucurestisector3': [('park_lake', 'Park Lake'),
                         ('unirea_shopping_center', 'Unirea Shopping Center')],

    'bucurestisector4': [('sun_plaza', 'Sun Plaza')],

    'bucurestisector5': [('vulcan_value_center', 'Vulcan Value Center')],

    'bucurestisector6': [('plaza_romania', 'Plaza Romania'),
                         ('afi_cotroceni', 'AFI Cotroceni'),
                         ('militari_shopping', 'Militari Shopping')], 

    'clujnapoca': [('iulius_mall', 'Iulius Mall'),
                   ('shopping_city', 'Shopping City Cluj')],
    'craiova': [('electroputere_mall', 'Electroputere Mall'),
                ('promenada_mall', 'Promenada Mall')],
    'iasi': [('palas_mall', 'Palas Mall')],
    'timisoara': [('iulius_town', 'Iulius Town')],
    'albaiulia': [('alba_mall', 'Alba Mall'),
                  ('mercur_city_center', 'Mercur City Center')],
    'arad': [('atrium_mall', 'Atrium Mall'),
            ('afi_arad', 'AFI Arad')], 
    'bacau': [('arena_mall', 'Arena Mall')],
    'brasov': [('afi_brsov', 'AFI Brasov'),
               ('coresi_shopping_resort', 'Coresi Shopping Resort')],
    'buzau': [('shopping_city_buzau', 'Shopping City Buzau')],
    'constanta': [('city_park_mall', 'City Park Mall'),
                  ('vivo_constanta','VIVO! Constanta')],
    'deva': [('shopping_city_deva', 'Shopping City Deva')],                
    'galati': [('shopping_city', 'Shopping City')],
    'oradea': [('lotus_center', 'Lotus Center'),
               ('oradea_shopping_city', 'Oradea Shopping City')],
    'pitesti': [('mall_vivo_pitesti', 'Mall VIVO! Pitesti'),
                ('supernova_pitesti', 'Supernova Pitesti')], 
    'piatraneamt': [('shopping_city_piatra_neamt', 'Shopping City Piatra Neamt')],
    'ploiesti': [('ploiesti_shopping_city', 'Poiesti Shopping City'),
                 ('afi_ploiestu','AFI Ploiesti')],
    'ramnicuvalcea': [('shopping_city_ramnicu_valcea', 'Shopping City Ramnicu Valcea'),
                      ('river_plaza_mall', 'River Plaza Mall')], 
    'sibiu': [('shopping_city_sibiu', 'Shopping City Sibiu'),
              ('promenada_mall_sibiu', 'Promenada Mall Sibiu')],
    'suceava': [('iulius_mall_suceava', 'Iulius Mall Suceava')],
    'targujiu': [('shopping_city_targujiu', 'Shopping City Targu Jiu')], 
    'targumures': [('targu_mures_shopping_city', 'Targu Mures Shopping City')],
    'severin': [('severin_shopping_center', 'Severin Shopping Center')]                                            
    }


class CustomUserCreationForm(UserCreationForm):
    CITY_CHOICES = [
        ('albaiulia', 'Alba Iulia'),
        ('arad', 'Arad'),
        ('bacau', 'Bacău'),
        ('brasov', 'Brașov'),
        ('bucurestisector1', 'București sector 1'),
        ('bucurestisector2', 'București sector 2'),
        ('bucurestisector3', 'București sector 3'),
        ('bucurestisector4', 'București sector 4'),
        ('bucurestisector5', 'București sector 5'),
        ('bucurestisector6', 'București sector 6'),
        ('buzau', 'Buzău'),
        ('clujnapoca', 'Cluj-Napoca'),
        ('constanta', 'Constanța'),
        ('craiova', 'Craiova'),
        ('deva', 'Deva'),
        ('galati', 'Galați'),
        ('iasi', 'Iași'),
        ('oradea', 'Oradea'),
        ('pitesti', 'Pitești'),
        ('piatraneamt', 'Piatra Neamț'),
        ('ploiesti', 'Ploiești'),
        ('ramnicuvalcea', 'Râmnicu Vâlcea'),
        ('sibiu', 'Sibiu'),
        ('suceava', 'Suceava'),
        ('targujiu', 'Târgu Jiu'),
        ('targumures', 'Târgu Mureș'),
        ('timisoara', 'Timișoara'),
        ('severin', 'Severin'),
    ]

    username = forms.CharField(
        label="Nume utilizator",
        help_text="Obligatoriu. 150 de caractere sau mai puțin. Doar litere, cifre și @/./+/-/_."
    )
    password1 = forms.CharField(
        label="Parolă",
        widget=forms.PasswordInput,
        help_text="<ul>"
                  "<li>Parola nu poate fi prea asemănătoare cu informațiile personale.</li>"
                  "<li>Parola trebuie să conțină cel puțin 8 caractere.</li>"
                  "<li>Parola nu poate fi una utilizată frecvent.</li>"
                  "<li>Parola nu poate fi exclusiv numerică.</li>"
                  "</ul>"
    )
    password2 = forms.CharField(
        label="Confirmare parolă",
        widget=forms.PasswordInput,
        help_text="Introduceți aceeași parolă ca mai sus, pentru verificare."
    )
    
    city = forms.ChoiceField(
        label="Oraș",
        choices=[('', 'Alege un oraș')] + CITY_CHOICES, 
        required=True
    )
    shopping_center = forms.ChoiceField(
        label="Centru comercial",
        choices=[('', 'Selectează centru comercial')],
        required=True
    )
    
    first_name = forms.CharField(label="Prenume", max_length=50)
    last_name = forms.CharField(label="Nume", max_length=50)
    store_name = forms.CharField(label="Nume magazin", max_length=100, required=True)
    phone_number = forms.CharField(label="Număr de telefon", max_length=20)
    email = forms.EmailField(label="Email")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2', 'city', 'shopping_center', 'store_name']


    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['shopping_center'].choices = [('', 'Selectează centru comercial')]
            if self.data.get('city'):
                city = self.data.get('city')
                self.fields['shopping_center'].choices = (
                    [('', 'Selectează centru comercial')] + 
                    SHOPPING_CENTERS.get(city, [])
                )

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        shopping_center = cleaned_data.get('shopping_center')
        if city and shopping_center:
            valid_centers = [mall[0] for mall in SHOPPING_CENTERS.get(city, [])]
            if shopping_center not in valid_centers:
                self.add_error('shopping_center', 'Centrul comercial selectat nu este disponibil în orașul ales.')
                
        return cleaned_data
