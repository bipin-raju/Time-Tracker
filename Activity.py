import datetime
import json
from dateutil import parser


class AcitivyList:
    def __init__(self, activities):
        self.activities = activities
    
    def initialize_me(self):
        activity_list = AcitivyList([])
        with open('activities.json', 'r') as f:
            data = json.load(f)
            activity_list = AcitivyList(
                activities = self.get_activities_from_json(data)
            )
        return activity_list
    
    def get_activities_from_json(self, data):
        return_list = []
        for activity in data['activities']:
            return_list.append(
                Activity(
                    app_name = activity['app_name'],
                    tasks = self.get_task_entries_from_json(activity)
                )
            )
        self.activities = return_list
        return return_list

    def get_task_entries_from_json(self, data):
        return_list = []
        for task in data['tasks']:
            return_list.append(
                Task(
                    task_name = task['task_name'],
                    time_entries = self.get_time_entires_from_json(task),
                )
            )
        self.activities = return_list
        return return_list
    
    def get_time_entires_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start_time = parser.parse(entry['start_time']),
                    end_time = parser.parse(entry['end_time'])
                )
            )
        self.time_entries = return_list
        return return_list
    
    def serialize(self):
        return {
            'activities' : self.activities_to_json()
        }
    
    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())
        
        return activities_


class Activity:
    def __init__(self, app_name, tasks):
        self.app_name = app_name
        self.tasks = tasks

    def serialize(self):
        return {
            'app_name' : self.app_name,
            'tasks' : self.make_task_entires_to_json()
        }
    
    def make_task_entires_to_json(self):
        task_list = []
        for task in self.tasks:
            task_list.append(task.serialize())
        return task_list


class Task:
    def __init__(self, task_name, time_entries):
        self.task_name = task_name
        self.time_entries = time_entries

    def serialize(self):
        return {
            'task_name' : self.task_name,
            'time_entries' : self.make_time_entires_to_json()
        }

    def make_time_entires_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())
        return time_list

class TimeEntry:
    def __init__(self, start_time, end_time):
        # self.start_time = start_time.replace(microsecond=0)
        # self.end_time = end_time.replace(microsecond=0)
        self.total_time = end_time - start_time
        # self.total_time = datetime.datetime.combine(datetime.datetime.min,end_time) \
        # - datetime.datetime.combine(datetime.datetime.min,start_time)
                
    def serialize(self):
        return {
            'start_time' : self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time' : self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_time' : ((str(self.total_time)).split('.'))[0]
        }