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
    ads = Ad.objects.filter(user=request.user)
    return render(request, 'ads_list.html', {'ads': ads})

@login_required
def upload_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            if hasattr(form.instance, 'video') and form.instance.video:
                ad.video = form.instance.video
                ad.image = None
            ad.save()
            return redirect("ads_list") 
    else:
        form = AdForm()
    return render(request, "upload_ad.html", {"form": form})

@login_required
def open_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("success_page")
    else:
        form = TicketForm()
    return render(request, "open_ticket.html", {"form": form})

def success_page(request):
    return render(request, 'success.html')

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if ad.image:  
        ad.image.delete(save=False)
    ad.delete()
    return redirect('ads_list')

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_tickets.html', {'tickets': tickets})

@staff_member_required
def launch_emotion_detection(request):
    if request.method == 'POST':
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test_webcam.py')
        subprocess.Popen([sys.executable, script_path])
        context = {'launched': True}
        return render(request, 'admin/emotion_detection.html', context)
    
    return render(request, 'admin/emotion_detection.html', {'launched': False})
