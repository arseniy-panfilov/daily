from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from django.utils.timezone import localtime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Area, Task, Interval
from .forms import AreaForm, TaskForm
import pytz

def index(request):
    if request.method == 'POST':
        if request.POST.get('add_area'):
            form = AreaForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['your_name']
                Area.add(name)
        elif request.POST.get('add_task'):
            add_task(request)
        elif request.POST.get('start_interval') or request.POST.get('end_interval'):
            add_interval(request)
        elif request.POST.get('export'):
            today = localtime(timezone.now())
            today_intervals = Interval.objects.filter(start__date=today)
            for interval in today_intervals:
                if not interval.end:
                    interval.end = timezone.now()
                print("Exporting")
                print(interval)
                interval.export()
            return redirect('daily:index')
        return redirect('daily:index')
    else:
        timezone.activate(pytz.timezone("Australia/Sydney"))
        today = localtime(timezone.now())
        today_areas_list = Area.objects.filter(date__date=today)
        return render(request, 'daily/index.html', {
            'area_form': AreaForm(),
            'task_form': TaskForm(),
            'today_areas_list': today_areas_list,
            'today_date': today,
        })
        
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        try:
            area = Area.objects.get(pk=request.POST['area_choice'])
            if not form.data['your_name']:
                raise Exception()
        except (KeyError, Area.DoesNotExist):
            messages.error(request, 'You didn\'t select an Area to add a Task to')
        except (Exception):
            messages.error(request, 'You didn\'t enter a name for the Task')
        else:
            if form.is_valid():
                name = form.cleaned_data['your_name']
                task = Task.add(name, area, 0)
    return redirect('daily:index')
    
def add_interval(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        try:
            if request.POST['task_choice']:
                task = Task.objects.get(pk=request.POST['task_choice'])
            else:
                raise Exception()
        except:
            messages.error(request, 'You didn\'t select a Task to add an Interval to')
        else:
            if 'start_interval' in request.POST:
                Interval.stop_active_interval(task)
                Interval.add(task)
            elif 'end_interval' in request.POST:
                Interval.stop_active_interval(task)
    return redirect('daily:index')

class IndexView(generic.ListView):
    template_name = 'daily/index.html'
    context_object_name = 'today_areas_list'

    def get_queryset(self):
        """
        Return all Areas for a given day
        """
        return Area.objects.filter(
            date__day=timezone.now().day
        ).order_by('date')