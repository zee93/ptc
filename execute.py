import json
import simplejson
import time


def create_project(p_name, p_estimatedtime, details=''):
    project = {
        'estimated time': p_estimatedtime,
        'details': details,
        'state': 'OFF',
        'total_spent_time': 0
    }

    with open('data/projects.json', 'r+') as p_file:
        projects = json.load(p_file)
        p_file.seek(0)
        p_file.truncate()
        projects.update({p_name: project})
        p_file.write(simplejson.dumps(projects, indent=4))
    with open('data/logs/{}.json'.format(p_name), 'w') as p_file:
        p_file.write('[]')

    print('project created.')

def start_timer_on_project(p_name):
    now = time.ctime().split()[-2]
    with open('data/projects.json', 'r') as p_file:
        projects = json.load(p_file)
        if projects.get(p_name) == None:
            print("We don't have a project with this name dear.")
            return 0
    with open('data/logs/{}.json'.format(p_name), 'r+') as logs_file:
        logs = json.load(logs_file)
        logs_file.seek(0)
        logs_file.truncate()
        logs.append({'start': now, 'end': 'not yet'})
        logs_file.write(simplejson.dumps(logs, indent=4))

    with open('data/settings.json', 'r+') as settings_file:
        settings = json.load(settings_file)
        settings_file.seek(0)
        settings_file.truncate()
        settings["working on"] = p_name
        settings_file.write(simplejson.dumps(settings, indent=4, sort_keys=True))

def stop_timer_on_project():
    with open('data/settings.json', 'r') as settings_file:
        settings = json.load(settings_file)
        p_name = settings["working on"]

    with open('data/logs/{}.json'.format(p_name), 'r+') as logs_file:
        logs = json.load(logs_file)
        logs_file.seek(0)
        logs_file.truncate()
        logs[-1]["end"] = time.ctime().split()[-2]
        logs_file.write(simplejson.dumps(logs, indent=4, sort_keys=True))


def execute_from_command_line(commands):
    if commands[0] == "createp":
        print("Creating project...")
        create_project(commands[1], commands[2], commands[3])

    elif commands[0] == "start":
        print("Happy coding...")
        start_timer_on_project(commands[1])

    elif commands[0] == "stop":
        print("Stoping timer...")
        stop_timer_on_project()

