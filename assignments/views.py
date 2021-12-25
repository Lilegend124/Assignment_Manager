from __future__ import print_function
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.template import loader
from django.utils import timezone
from .drive_API import main
from . import views
from .models import To_Do_Item, Event_Item, Class_Item, User, Document
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
from django.urls import reverse_lazy
import datetime
from urllib.request import urlopen
import datetime
from datetime import timedelta
import os.path
import json
from django.views import View
from . import forms

from .calendar_API import add_event_to_calendar

# Default, simply text
# def index(request):
#     return HttpResponse("Hello, world. You have reached Assignment manager.")

class index(View):
    def get(self, request):
        context = dict()
        try:
            context['to_do_items'] = To_Do_Item.objects.filter(author=self.request.user)
            context['event_items'] = Event_Item.objects.filter(author=self.request.user)
            return render(request, 'index.html', context)
        except:
            return render(request, 'index.html')

################################################################
#################### TO DO START ############################
################################################################

class To_Do_List_View(LoginRequiredMixin, ListView):
    model = To_Do_Item
    template_name = 'to_do_list.html'
    context_object_name = 'to_do_items'

    def get_queryset(self):
        return To_Do_Item.objects.filter(author=self.request.user)

class To_Do_Detail_View(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = To_Do_Item
    template_name = 'to_do_detail.html'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class To_Do_Create_View(LoginRequiredMixin, CreateView):
    model = To_Do_Item
    fields = ['title','content','date']
    template_name = 'to_do_create.html'
    success_url = reverse_lazy('day')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_form(self):
        from django import forms
        form = super(To_Do_Create_View, self).get_form()
        form.fields['date'] = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'])
        return form
    
class To_Do_Update_View(LoginRequiredMixin, UpdateView):
    model = To_Do_Item
    fields = ['title','content','date']
    template_name = 'to_do_create.html'
    success_url = reverse_lazy('day')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    # def get_form(self):
    #     from django import forms
    #     form = super(To_Do_Create_View, self).get_form()
    #     form.fields['start'] = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'])
    #     form.fields['end'] = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'])
    #     return form

class To_Do_Delete_View(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = To_Do_Item
    success_url = reverse_lazy('day')
    template_name = "to_do_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

################################################################
#################### Day/Calendar Views ########################
################################################################
#def request_page(request):
#  if(request.GET.get('calendar')):
#      add_event_to_calendar("test", '2021-11-01T09:00:00-07:00', '2021-11-01T10:00:00-07:00')
# in day.html
#<form action="#" method="get">
 #                           <input type="submit" class="btn btn-secondary btn-lg" value="Add to Calendar" name="calendar/">
  #                      </form>

# Two diff functions below because event and due date are two different models
# This is for adding an event under schedule to calendar

def calendar_schedule(request, calendar_schedule_id):
    # need to change the below parameters by accessing the fields of the to do list or schedule
    calendarObject = get_object_or_404(Event_Item, pk = calendar_schedule_id)
    results = add_event_to_calendar(calendarObject.title, calendarObject.start.isoformat(), calendarObject.end.isoformat(), request)  #https://www.kite.com/python/answers/how-to-write-a-datetime-object-to-json-in-python
    context = {"results": results}
    return render(request, 'calendar.html', context)


# This is for adding an event under due date to calendar
def calendar(request, calendar_id):
    # need to change the below parameters by accessing the fields of the to do list or schedule
    calendarObject = get_object_or_404(To_Do_Item, pk = calendar_id)  #https://www.geeksforgeeks.org/get_object_or_404-method-in-django-models/
    results = add_event_to_calendar(calendarObject.title, calendarObject.date.isoformat(), calendarObject.date.isoformat(), request)
    context = {"results": results}
    return render(request, 'calendar.html', context)


'''
def demo(request):
    results = test_calendar()
    context = {"results": results}
    return render(request, 'demo.html', context)
'''

class Day_View(LoginRequiredMixin, View):

    def get(self, request):
        context = dict()
        context['to_do_items'] = To_Do_Item.objects.filter(author=self.request.user)
        context['event_items'] = Event_Item.objects.filter(author=self.request.user)
        context['form'] = forms.DateForm(self.request.GET)
        return render(request, 'day.html', context)

    def get_queryset(self):
        """
        Dummy function that is not really needed?
        """
        pass


    def post(self, request):
        form = forms.DateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            context = dict()
            to_do_objects = To_Do_Item.objects.filter(date__year=date.year,
                                   date__month=date.month,
                                   date__day=date.day,
                                   author=self.request.user)
            event_items = Event_Item.objects.filter(end__year=date.year,
                                   end__month=date.month,
                                   end__day=date.day,
                                   author=self.request.user)
            context['to_do_items'] = to_do_objects
            context['event_items'] = event_items
            context['form'] = forms.DateForm(self.request.GET)
            return render(request, 'day.html', context)
        else:
            context = dict()
            context['to_do_items'] = To_Do_Item.objects.filter(author=self.request.user)
            context['event_items'] = Event_Item.objects.filter(author=self.request.user)
            context['form'] = forms.DateForm(self.request.GET)
            return render(request, 'day.html', context)

#########################################################
#################### Event Views ########################
#########################################################

class Event_List_View(LoginRequiredMixin, ListView):
    model = Event_Item
    template_name = 'event_list.html'
    context_object_name = 'event_items'

    def get_queryset(self):
        return Event_Item.objects.filter(author=self.request.user)


class Event_Detail_View(LoginRequiredMixin, DetailView):
    model = Event_Item
    template_name = 'event_detail.html'


class Event_Create_View(LoginRequiredMixin, CreateView):
    model = Event_Item
    fields = ['title', 'start', 'end']
    template_name = 'event_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Event_Update_View(LoginRequiredMixin, UpdateView):
    model = Event_Item
    fields = ['title', 'start', 'end']
    template_name = 'event_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Event_Delete_View(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event_Item
    success_url = reverse_lazy('day')
    template_name = "event_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def drive(request):
    results = main()
    context = {"results": results}
    return render(request, 'drive.html', context)

def day(request):
    return render(request, 'day.html')


def view_name(request):
    return render(request, 'assignments.html', {})

urlpatterns = [
    path('', views.view_name, name="view_name"),
]

#########################################################
################### Classes Views #######################
#########################################################
class Class_view(LoginRequiredMixin, View):
    def get(self, request):
        context = dict()
        context['to_do_items'] = To_Do_Item.objects.filter(author=self.request.user)
        context['event_items'] = Event_Item.objects.filter(author=self.request.user)
        user = request.user
        context['class_items'] = user.classes.all()
        return render(request, 'classes.html', context)

class Classes_View_Users(LoginRequiredMixin, View):
    def get(self, request, pk):
        context = dict()
        get_class = Class_Item.objects.get(pk=pk)
        all_users = User.objects.all()
        users = []
        for user in all_users:
            if get_class in user.classes.all():
                users.append(user)
        context['class_users'] = users
        return render(request, 'classes_view_users.html', context)

class Classes_Add_View(LoginRequiredMixin, ListView):
    model = Class_Item
    template_name = 'classes_add.html'
    context_object_name = 'class_items'

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            postresult = Class_Item.objects.filter(class_title__contains=query)
            result = postresult
        else:
            result = Class_Item.objects.all()
        return result


class Classes_Detail_View(LoginRequiredMixin, View):
    def get(self, request, pk):
        context = dict()
        class_item = Class_Item.objects.get(id=pk)
        context['documents'] = Document.objects.filter(class_item=pk)
        context['class_item'] = class_item
        return render(request, 'classes_detail.html', context)


class Classes_Create_View(LoginRequiredMixin, CreateView):
    model = Class_Item
    template_name = 'classes_create.html'
    fields = ['class_title', 'meeting_days']

    def form_valid(self, form):
        # users = User.objects.filter(self)
        # instance = Class_Item.objects.create()

        # form.instance.author = self.request.user
        return super().form_valid(form)


class Classes_Delete_View(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Class_Item
    success_url = reverse_lazy('day')
    template_name = "to_do_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    template_name = 'classes_detail.html'

def add_class(request, pk):
    # need to change the below parameters by accessing the fields of the to do list or schedule
    Class_to_add = get_object_or_404(Class_Item, pk = pk)  #https://www.geeksforgeeks.org/get_object_or_404-method-in-django-models/
    user = request.user
    user.classes.add(Class_to_add)
    context = {'class_items': user.classes.all()}
    return render(request, 'classes.html', context)


#########################################################
################### Upload File #######################
#########################################################

from .forms import UploadFileForm
from django.forms import HiddenInput
from django.http import HttpResponseRedirect
from django.urls import reverse

def upload_file(request, pk):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('classes_detail', args=[pk]))
    else:
        form = UploadFileForm()
        form.fields['class_item'].widget = HiddenInput()
        form.fields['class_item'].initial = get_object_or_404(Class_Item, pk = pk)
        form.fields['author'].widget = HiddenInput()
        form.fields['author'].initial = get_object_or_404(User, pk = request.user)
    return render(request, 'upload.html', {'form': form})

class All_Documents_View(LoginRequiredMixin, View):
    def get(self, request):
        context = dict()
        context['documents'] = Document.objects.all()
        return render(request, 'documents.html', context)

class Document_Delete_View(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    success_url = reverse_lazy('classes')
    template_name = "document_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

