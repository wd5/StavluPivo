# -*- coding:utf-8 -*-
from django.db import models
from my_auth.models import User

# Create your models here.

class TaskGroup(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=256, null = False)

class Task(models.Model):
    parent_task = models.ForeignKey('self', null = False)
    group = models.ForeignKey(TaskGroup, null = True)
    name = models.CharField(max_length=256, blank = True)
    performers = models.ManyToManyField(User)                     # исполнители

    ## time conditions 
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    start = models.DateTimeField(null=True)
    stop = models.DateTimeField(null=True)
    sheduler_stop = models.DateTimeField(null=True)               # запланированное дата остановки
    man_minuts = models.PositiveIntegerField(null=False)
    
    def save(self):
        super(Task,self).save()
        if not self.name:
            self.name='task_'+str(self.id)
        
class WallTask(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=32, null = False)
    text_task = models.TextField()
    position_x = models.IntegerField(null=False)
    position_y = models.IntegerField(null=False)
