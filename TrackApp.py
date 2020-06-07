import win32gui
import time
import psutil
import win32process
import psutil
import uiautomation as auto
import datetime
# from Activity import *
from DataBaseAdapter import DataBaseAdapter


first_run = True
start_time = datetime.datetime.now()
end_time = datetime.datetime.now()
current_work = ""
activity_entry = ""
task_entry = ""
# activityList = AcitivyList([])
db = DataBaseAdapter()


def get_site_from_url(url):    
    string_list = url.split('/')
    if "https:" in string_list:
        domain = string_list[2]
    else:
        domain = string_list[0]

    site = domain.split('.')
    if(site[0] == "www"):
        return site[1].title()
    else:
        return site[0].title()


def get_chrome_url():
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    try:
        url = edit.GetValuePattern().Value
    except (AttributeError, LookupError) as e:
        url = None
        print("Error trying to fetch url")
        print(e)
        
    if url is None:
        print("URL fetched is empty. Not logging this activity")
        return ""
    else:
        return get_site_from_url(url)


def get_current_task(app_name, window_title):
    task = window_title
    if app_name == "msedge.exe":
        task = get_chrome_url()   
    elif app_name == "explorer.exe":
        if "% complete" in window_title:
            task = "File Transfer"            
    elif app_name == "Code.exe":
        project_name = window_title.split(' - ')
        if(len(project_name) > 1):
            task = project_name[1]
        else:
            task = project_name[0]
    elif app_name == "cmd.exe":
        task = ""     

    task.replace('*', '')
    return task

'''
def log_activity(task_entry, activity_entry):
    global activityList
    global start_time
    global end_time

    time_entry = TimeEntry(start_time, end_time)
    # print(time_entry.total_time)
    if(time_entry.total_time < datetime.timedelta(seconds=5)):
        return
    
    min = round((time_entry.total_time.seconds/60), 2)
    #print(str(start_time) + "  -  " + str(end_time))
    print(current_activity + " \t\t<|> " + current_task + "\t\t<|> " + str(min))
    new_task = Task(task_entry, [time_entry])
    activity_exists = False
    for activity in activityList.activities:
        if activity.app_name == activity_entry:
            activity_exists = True
            task_exists = False
            for task in activity.tasks:
                if task.task_name == task_entry:
                    task_exists = True
                    task.time_entries.append(time_entry)
                    break
                
            if task_exists == False:
                activity.tasks.append(new_task)

    if not activity_exists:
        activity = Activity(activity_entry, [new_task])
        activityList.activities.append(activity)

    with open('activities.json', 'w') as json_file:
        json.dump(activityList.serialize(), json_file,
                    indent=4, sort_keys=True)
    start_time = datetime.datetime.now()
'''    


def log_activity_in_DB(task_entry, activity_entry):
    global db
    global start_time
    global end_time

    start_time  = start_time.replace(microsecond=0)
    end_time    = end_time.replace(microsecond=0)
    total_time  = end_time - start_time
    if(total_time < datetime.timedelta(seconds=5)):
        return

    min = round((total_time.seconds/60), 2)
    print(activity_entry + " \t\t<|> " + task_entry + "\t\t<|> " + str(min))    
    db.execute_query(db.insert_activity.format(datetime.date.today(), activity_entry, 1, task_entry, start_time.time(), end_time.time(), total_time.seconds))
    # print(insert_activity.format(datetime.date.today(), activity_entry, 1, task_entry, start_time.time(), end_time.time(), time_entry.total_time.seconds))
    start_time = datetime.datetime.now()

## Starts here ################
# try:
# activityList.initialize_me()
db.execute_query(db.create_todays_table.format(datetime.date.today()))
# except Exception:
    # print('Exception: No json')

while True:
    time.sleep(5)
    window_title        = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    pid                 = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())    

    try:        
        process_name        = psutil.Process(pid[-1]).name()        
    except (psutil.NoSuchProcess, ValueError) as e:
        print("Exception occured in window : " + window_title)
        print(e)
        continue

    current_task        = get_current_task(process_name, window_title) 
    current_activity    = process_name   

    if current_activity not in current_work or current_task not in current_work:
        current_work = current_activity + " \t\t<|> " + current_task
        if first_run:
            first_run = False
            #in order to find the run time of first app, need to wait till switch happens to next app
            #therefore log activity_entry and task_entry instead of current_activity and current_task 
        else:
            end_time = datetime.datetime.now()
            # log_activity(task_entry, activity_entry)
            log_activity_in_DB(task_entry, activity_entry)
        activity_entry = current_activity
        task_entry = current_task
