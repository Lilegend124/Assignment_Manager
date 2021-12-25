from django.urls import path
from django.contrib import admin
from django.contrib.sites.models import Site

from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('to_do/', views.To_Do_List_View.as_view(), name='to_do_list'),
    #path('calendar/', views.calendar, name='calendar'),
    path('day/', views.Day_View.as_view(), name='day'),
    path('drive/', views.drive, name='drive'),
    path('day/', views.day, name='day'),
    path('to_do/<int:pk>/', views.To_Do_Detail_View.as_view(), name='to_do_detail'),
    path('to_do/<int:pk>/update', views.To_Do_Update_View.as_view(), name='to_do_update'),
    path('to_do/<int:pk>/delete', views.To_Do_Delete_View.as_view(), name='to_do_delete'),
    path('to_do/create/', views.To_Do_Create_View.as_view(), name='to_do_create'),
    path('event/<int:pk>/', views.Event_Detail_View.as_view(), name='event_detail'),
    path('event/<int:pk>/update', views.Event_Update_View.as_view(), name='event_update'),
    path('event/create/', views.Event_Create_View.as_view(), name='event_create'),
    path('event/<int:pk>/delete', views.Event_Delete_View.as_view(), name='event_delete'),
    path('classes/', views.Class_view.as_view(), name='classes'),
    path('classes/add/', views.Classes_Add_View.as_view(), name='classes_add'),
    path('classes/add_class/<int:pk>/', views.add_class, name='classes_add_class'),
    path('classes/<int:pk>/', views.Classes_Detail_View.as_view(), name='classes_detail'),
    path('classes/view_users/<int:pk>/', views.Classes_View_Users.as_view(), name='classes_view_user'),
    path('classes/create/', views.Classes_Create_View.as_view(), name='classes_create'),

    path('calendar/<int:calendar_id>', views.calendar, name='add_to_calendar'),
    path('calendar_schedule/<int:calendar_schedule_id>', views.calendar_schedule, name='add_to_calendar_schedule'),

    path('upload_file/<int:pk>', views.upload_file, name='upload_file'),
    path('document/<int:pk>/delete', views.Document_Delete_View.as_view(), name='document_delete'),
    path('all_documents/', views.All_Documents_View.as_view(), name='all_ducuments'),
    #path('demo/', views.demo, name='demo'),

]

admin.site.unregister(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'domain')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')
admin.site.register(Site, SiteAdmin)

# All this code comes from: https://stackoverflow.com/questions/25468676/django-sites-model-what-is-and-why-is-site-id-1
