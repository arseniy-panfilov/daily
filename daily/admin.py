from django.contrib import admin

from .models import Area, Task, Interval

# Register your models here.
admin.site.register(Area)
admin.site.register(Task)
admin.site.register(Interval)
