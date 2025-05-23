from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Ad, Ticket
from .forms import AdForm
from .forms import TicketForm
from django.http import JsonResponse
from django.http import HttpResponse
import subprocess
import os
import sys
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def ads_list(request):
    ads = Ad.objects.filter(user=request.user)  # aici se preiau reclamele
    return render(request, 'ads_list.html', {'ads': ads})

@login_required
def upload_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)  #procesare formular
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user  #asociaza reclama cu utilizatorul curent

            # verifica daca este un fisier video in instanta, setat în clean_image
            if hasattr(form.instance, 'video') and form.instance.video:
                ad.video = form.instance.video
                ad.image = None  #resetam imaginea daca avem video

            ad.save()
            return redirect("ads_list")  #redirectioneaza catre lista de reclame
    else:
        form = AdForm()  #formularul gol pentru GET request

    return render(request, "upload_ad.html", {"form": form})


@login_required
def open_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  #asociaza tichetul cu utilizatorul logat
            ticket.save()
            return redirect("success_page")
    else:
        form = TicketForm()
    return render(request, "open_ticket.html", {"form": form})

def success_page(request):
    return render(request, 'success.html')

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)  #se asigura ca doar utilizatorul isi poate sterge reclama
    if ad.image:  
        ad.image.delete(save=False)  #sterge imaginea fizic din server

    ad.delete()  # sterge reclama din baza de date
    return redirect('ads_list')  # redirectioneaza utilizatorul inapoi la lista reclamelor


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_tickets.html', {'tickets': tickets})


@staff_member_required
def launch_emotion_detection(request):
    if request.method == 'POST':
        # preia calea catre scriptul cu modelul care clasifica emotiile
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test_webcam.py')
        # porneste scriptul intr un proces separat
        subprocess.Popen([sys.executable, script_path])
        
        context = {'launched': True}
        return render(request, 'admin/emotion_detection.html', context)
    
    return render(request, 'admin/emotion_detection.html', {'launched': False})