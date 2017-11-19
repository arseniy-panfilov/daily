from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime

import datetime

class System():
    def get_local_date():
        return localtime(timezone.now()).date()
    

class Area(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField('date')
    priority = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return self.name
    
    def add(name):
        """Creates a new Area for the date on which this function is called"""
        today = System.get_local_date()
        duplicates = Area.objects.filter(date__date=today).filter(name=name)
        if not duplicates.exists():
            return Area.objects.create(
                name=name,
                date=timezone.now()
            )

    
class Task(models.Model):
    name = models.CharField(max_length=50)
    priority = models.IntegerField(default=0)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return self.name
    
    def add(name, area, priority):
        """Adds a Task to a given Area"""
        duplicates = Task.objects.filter(name=name)
        if not duplicates.exists():
            return area.task_set.create(
                name=name,
                priority=priority
            )

    
class Interval(models.Model):
    start = models.DateTimeField('start time')
    end = models.DateTimeField('end time', null=True)
    duration = models.DurationField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    def add(task):
        """Creates and starts an Interval for the given Task"""
        interval = task.interval_set.create(
            start=timezone.now()
        )
        return interval

    def stop(self):
        self.end = timezone.now()
        self.update_duration()

    def update_duration(self):
        if self.end is None:
            self.duration = timezone.now() - start
        else:
            self.duration = self.end - self.start

    def stop_active_interval(task):
        intervals = task.interval_set.all()
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
