from django import forms
from django.contrib import admin
from .models import Ticket, Ad
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.html import format_html

class ResponseForm(forms.Form):
    response = forms.CharField(widget=forms.Textarea, label="Răspunsul tău")

class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "description", "status", "created_at", "has_response", "response_link")
    list_filter = ("status",)
    search_fields = ("user__username", "description")
    actions = ["mark_as_in_progress", "mark_as_resolved", "mark_as_closed"]
    
    def has_response(self, obj):
        return bool(obj.admin_response)
    has_response.boolean = True
    has_response.short_description = "Are răspuns"
    
    def response_link(self, obj):
        return format_html(
            '<a href="{}">Răspunde</a>',
            reverse('admin:respond_to_ticket', args=[obj.pk])
        )
    response_link.short_description = "Acțiune"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'respond/<int:ticket_id>/',
                self.admin_site.admin_view(self.respond_to_ticket),
                name='respond_to_ticket',
            ),
        ]
        return custom_urls + urls
    
    def respond_to_ticket(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        
        if request.method == 'POST':
            form = ResponseForm(request.POST)
            if form.is_valid():
                # salvam rsspunsul in ticket-ul existent
                ticket.admin_response = form.cleaned_data['response']
                ticket.response_date = timezone.now()
                ticket.status = 'resolved'
                ticket.save()
                
                # pentru debugging am scris aceste printuri
                print(f"Răspuns salvat pentru tichetul #{ticket.id}")
                print(f"Conținutul răspunsului: {ticket.admin_response}")
                
                self.message_user(request, f"Răspunsul a fost trimis pentru tichetul #{ticket.id}")
                return redirect('admin:website_ads_ticket_changelist')
        else:
            # pre-completeaza formularul cu raspunsul existent daca exista
            initial_data = {}
            if ticket.admin_response:
                initial_data['response'] = ticket.admin_response
            form = ResponseForm(initial=initial_data)
        
        context = {
            'title': f'Răspunde la tichetul #{ticket.id}',
            'ticket': ticket,
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/respond_to_ticket.html', context)
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Marchează ca În lucru"
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')
    mark_as_resolved.short_description = "Marchează ca Rezolvat"
    
    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
    mark_as_closed.short_description = "Marchează ca Închis"

# inregistram Ticket cu clasa TicketAdmin
admin.site.register(Ticket, TicketAdmin)




class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('emotion-detection-redirect/', self.admin_view(self.emotion_detection_redirect), 
                 name='emotion_detection_redirect'),
        ]
        return custom_urls + urls
    
    def emotion_detection_redirect(self, request):
        return redirect('emotion_detection')
   
    def each_context(self, request):
        context = super().each_context(request)
        context['emotion_detection_url'] = 'emotion-detection-redirect/'
        return context

admin_site = MyAdminSite(name='myadmin')