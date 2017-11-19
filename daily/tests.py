from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import localtime

from daily.models import System, Area, Task, Interval

# Create your tests here.
class AreaTestCase(TestCase):
    def setUp(self):
        Area.add('Programming')
        
    def test_area_added(self):
        areas_list = Area.objects.all()
        self.assertTrue(areas_list.count() == 1)
    
    def test_duplicates_not_added(self):
        Area.add('Programming')
        Area.add('Programming')
        Area.add('Programming')
        today = System.get_local_date()
        duplicates = Area.objects.filter(date__date=today).filter(name='Programming')
        self.assertTrue(duplicates.count() == 1)
        
class TaskTestCase(TestCase):
    def setUp(self):
        programming_area = Area.add('Programming')
        Task.add('Leetcode', programming_area, 0)
        Task.add('Will', programming_area, 0)
        life_area = Area.add('Life')
        Task.add('Visit dentist', life_area, 0)
        Task.add('Pay bills', life_area, 0)
    
    def test_output(self):
        today = localtime(timezone.now()).date()
        today_areas_list = Area.objects.all()
        # Translate all DateTimes into local time
        for area in today_areas_list:
            print(area)
            area.date = localtime(area.date)
            area_tasks_list = Task.objects.filter(area=area)
            for task in area_tasks_list:
                print("------" + task.name)

class IntervalTestCase(TestCase):
    def setUp(self):
        programming_area = Area.add('Programming')
        will_task = Task.add('Will', programming_area, 0)
        interval_1 = Interval.add(will_task)
        
    def test_interval_add(self):
        will_task = Task.objects.get(name='Will')
        intervals_list = Interval.objects.filter(task=will_task) 
        self.assertTrue(intervals_list.count() == 1)
        
    def test_interval_stop(self):
        will_task = Task.objects.get(name='Will')
        interval = Interval.objects.get(task=will_task) 
        interval.stop()
        self.assertTrue(interval.end is not None)
        self.assertTrue(interval.duration is not None)



