from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.models import User

from .gcal import GoogleCalendar

import datetime

class System():
    def get_local_date():
        return localtime(timezone.now()).date()
    

class Area(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField('date', default=datetime.date.today)
    priority = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = (('name', 'date'),) 
        ordering = ['date']
    
    def __str__(self):
        return self.name
    
    def add(name, user):
        """Creates a new Area for the date on which this function is called"""
        return Area.objects.create(
            name=name,
            user=user
        )

    
class Task(models.Model):
    name = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField(default=0)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return self.name
    
    def add(name, area, priority, user):
        """Adds a Task to a given Area"""
        return area.task_set.create(
            name=name,
            priority=priority,
            user=user
        )

    
class Interval(models.Model):
    start = models.DateTimeField('start time', default=timezone.now())
    end = models.DateTimeField('end time', null=True)
    duration = models.DurationField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def add(task, user):
        """Creates and starts an Interval for the given Task"""
        return task.interval_set.create(
            user=user
        )

    def stop(self):
        self.end = timezone.now()
        self.update_duration()

    def update_duration(self):
        if self.end is None:
            self.duration = timezone.now() - start
        else:
            self.duration = self.end - self.start
            
    def export(self):
        GoogleCalendar.add_interval_as_event(self)

    def stop_active_interval(task, user):
        intervals = task.interval_set.all().filter(user=user)
        for interval in intervals:
            if interval.end is None:
                interval.stop()
                interval.save()
                return

    def check_timed_out():
        """Automatically checks all intervals and adjusts their duration if not stopped"""
        today = System.get_local_date()
        today_intervals = Interval.objects.filter(start__date=today)
        for interval in today_intervals:
            interval.update_duration()
            if interval.end is None and (timezone.now() - interval.start) > datetime.timedelta(hours=4):
                # Stop the interval and set its duration to 1 hour
                interval.end = interval.start + datetime.timedelta(hours=1)
                interval.update_duration()
