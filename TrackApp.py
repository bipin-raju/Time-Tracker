import win32gui
import time
import psutil
import win32process
import psutil
import uiautomation as auto
import datetime
from Activity import *

def get_site_from_url(url):    
    string_list = url.split('/')
    if "https:" in string_list:
        return string_list[2]
    else:
        return string_list[0]


def get_chrome_url():
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    url = edit.GetValuePattern().Value
    if url is None:

        return ""
    else:
        return get_site_from_url(url)

def get_current_task(app_name, window_title):
    if app_name == "msedge.exe":
        task = get_chrome_url()   
    elif app_name == "Code.exe":
        project_name = window_title.split(' - ')
        if(len(project_name) > 1):
            task = project_name[1]
        else:
            task = project_name[0]
    elif app_name == "cmd.exe":
        task = ""     
    else:
        task = window_title
        window_title.replace('*', '')
    return task

# try:
first_run = True
start_time = datetime.datetime.now()
current_work = ""
activity_entry = ""
task_entry = ""
activeList = AcitivyList([])

try:
    activeList.initialize_me()
except Exception:
    print('No json')

while True:
    time.sleep(5)
    window_title        = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    pid                 = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())    

    try:        
        process_name        = psutil.Process(pid[-1]).name()        
    except (psutil.NoSuchProcess, ValueError) as e:
        print("Exception occured : " + e)
        continue


    current_task        = get_current_task(process_name, window_title) 
    current_activity    = process_name   

    if current_activity not in current_work or current_task not in current_work:
        current_work = current_activity + " \t\t<|> " + current_task
        print(current_work)

        if first_run:
            first_run = False
            #in order to find the run time of first app, need to wait till switch happens to next app
            #therefore log activity_entry and task_entry instead of current_activity and current_task 
        else:
            end_time = datetime.datetime.now()
            time_entry = TimeEntry(start_time, end_time)
            # print(time_entry.total_time)
            if(time_entry.total_time < datetime.timedelta(seconds=5)):
                continue
            task_enty = Task(task_entry, [time_entry])

            activity_exists = False
            for activity in activeList.activities:
                if activity.app_name == activity_entry:
                    activity_exists = True
                    task_exists = False
                    for task in activity.tasks:
                        if task.task_name == task_entry:
                            task_exists = True
                            task.time_entries.append(time_entry)
                            break
                        
                    if task_exists == False:
                        activity.tasks.append(task_enty)

            if not activity_exists:
                activity = Activity(activity_entry, [task_enty])
                activeList.activities.append(activity)
            with open('activities.json', 'w') as json_file:
                json.dump(activeList.serialize(), json_file,
                            indent=4, sort_keys=True)
                start_time = datetime.datetime.now()

        activity_entry = current_activity
        task_entry = current_task



# except Exception:
    # print("\n\n\n ==> Good bye then.")