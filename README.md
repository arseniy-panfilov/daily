# daily
A daily to do list with time tracking. Uses the Django framework.

Each day is organised into "Areas". These are high level categories of things that need to be done.

Each Area contains "Tasks". These are lower level tasks.

Each Task contains zero to many "Intervals". These are periods of time spent doing that particular task.

Example:

Programming  
---Work on daily  
------9.00 - 9.50  
------10.00 - 10.30  

By gathering up all these intervals, you'll be able to create a very accurate record of how you've spent your days.

Eventually there'll be automated exporting to Google Calendar, so that you'll be able to see all your intervals as entries.
