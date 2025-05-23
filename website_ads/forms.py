from django import forms
from .models import Ad
from .models import Ticket

class AdForm(forms.ModelForm):
    title = forms.CharField(label="Titlu")
    category = forms.ChoiceField(choices=Ad.CATEGORIES_CHOICES, label="Categorii reclame")
    image = forms.FileField(label="Imagine sau video")
    class Meta:
        model = Ad
        fields = ['title', 'category', 'image']

    def clean_image(self):
        file = self.cleaned_data.get('image')
        if file:
            # obtine extensia fisierului
            name = file.name.lower()
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            video_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.webm', '.mkv']
            
            # verific daca este video
            if any(name.endswith(ext) for ext in video_extensions):
                #fisierul este video si il vom salva in campul video in view
                self.instance.video = file
                return None  # aici nu salvam nimic în câmpul image
            
            #verifica daca este imagine
            elif any(name.endswith(ext) for ext in image_extensions):
                return file  #este imagine continuam normal
            
            # daca nu este nici imagine nici video acceptat afisez mesajul
            else:
                raise forms.ValidationError(
                    "Formatele de fișier acceptate sunt: " + 
                    ", ".join(image_extensions) + " pentru imagini și " + 
                    ", ".join(video_extensions) + " pentru videoclipuri."
                )
        return file   


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Descrie problema..."})
        }