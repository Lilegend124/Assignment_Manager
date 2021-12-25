from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class User(AbstractUser):
    username = models.CharField(_('username'), max_length=120)
    password = models.CharField(max_length=120)
    first_name = models.CharField(_('first name'), max_length=120, blank=True)
    last_name = models.CharField(_('last name'), max_length=120, blank=True)
    email = models.EmailField(_('email address'), primary_key=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    ACCOUNT_EMAIL_VERIFICATION = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    classes = models.ManyToManyField('Class_Item')

# Events appear on calendars
class Event_Item(models.Model):
    title = models.CharField(max_length=200)  # name of the class, meeting, etc.
    start = models.DateTimeField()  # start time as instance of datetime.datetime instance
    end = models.DateTimeField()  # end time as instance of datetime.datetime instance
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('day')

    def __str__(self):
        return self.title + " from: " + self.start + " to " + self.end

class To_Do_Item(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('to_do_list')
    def filter_author_date(self, author, date):
        return self.objects.filter(date__year=date.year,
                                   date__month=date.month,
                                   date__day=date.day,
                                   author=author)

class Class_Item(models.Model):
    class_title = models.CharField(max_length=300, default='temp')  # Name of the class
    meeting_days = models.CharField(max_length=300) # days the class is on
    prof = models.CharField(max_length=300)  # professor of the class
    mnemonic = models.CharField(max_length=300)  # class mnemonic (CS, PHIL, etc)
    class_number = models.CharField(max_length=300)  # number of the class
    semester = models.CharField(max_length=300)
    meeting_time_start = models.TimeField(default=None)  # start time as instance of datetime.datetime instance
    meeting_time_end = models.TimeField(default=None)  # end time as instance of datetime.datetime instance

    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # students = ArrayField(models.CharField(max_length=100, blank=True),size=500,)
    # student = models.CharField(max_length=300)
    def get_absolute_url(self):
        return reverse('classes')

    def __str__(self):
        if self.meeting_time_start.minute == 0:
            startminute = "00"
        else:
            startminute = self.meeting_time_start.minute

        if self.meeting_time_start.minute == 0:
            endminute = "00"
        else:
            endminute = self.meeting_time_start.minute



        return f"{self.class_title} ({self.semester}, {self.mnemonic} {self.class_number}, " \
               f"{self.meeting_days} {self.meeting_time_start.hour}:{startminute}-{self.meeting_time_end.hour}:{endminute}) taught by {self.prof}"

class Document(models.Model):
    name = models.CharField(max_length=100, default='temp')
    doc = models.FileField(upload_to='save_file_dir')
    class_item = models.ForeignKey(Class_Item, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


