from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from django.utils.timezone import localtime
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Area, Task, Interval
from .forms import AreaForm, TaskForm

def index(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            Area.add(name)
            return redirect('daily:index')
    else:
        today = localtime(timezone.now()).date()
        today_areas_list = Area.objects.filter(date__date=today)
        # Translate all DateTimes into local time
        for area in today_areas_list:
            area.date = localtime(area.date)
        return render(request, 'daily/index.html', {
            'area_form': AreaForm(),
            'task_form': TaskForm(),
            'today_areas_list': today_areas_list,
            'today_date': today,
        })
        
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        area = Area.objects.get(pk=request.POST['choice'])
        if form.is_valid():
            name = form.cleaned_data['your_name']
            task = Task.add(name, area, 0)
            print(task)
            return redirect('daily:index')
    else:
        return redirect('daily:index')
    
def add_interval(request):
    if request.method == 'POST':
        if 'start' in request.POST:
            task = Task.objects.get(pk=request.POST['choice'])
            Interval.stop_active_interval(task)
            Interval.add(task)
        elif 'end' in request.POST:
            task = Task.objects.get(pk=request.POST['choice'])
            Interval.stop_active_interval(task)
        return redirect('daily:index')
    else:
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