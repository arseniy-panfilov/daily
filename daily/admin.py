from django.contrib import admin

from .models import Area, Task, Interval

# Register your models here.
@admin.register(Area)
class AreaInstanceAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class TaskInstanceAdmin(admin.ModelAdmin):
    pass

@admin.register(Interval)
class IntervalInstanceAdmin(admin.ModelAdmin):
    pass
