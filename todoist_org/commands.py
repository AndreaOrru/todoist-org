#!/usr/bin/env python

from collections import defaultdict
from os import environ as env

import todoist
from PyOrgMode import PyOrgMode

from . import items, projects

api = todoist.TodoistAPI(env['TODOIST_API_TOKEN'])
api.sync()


def download(filename):
    base = PyOrgMode.OrgDataStructure()

    projectItems = defaultdict(list)
    for item in items.from_todoist(api.items.all()):
        projectItems[item.project_id].append(item)

    for project in projects.from_todoist(api.projects.all()):
        orgProject = project.to_org()
        for item in projectItems[project.id]:
            orgProject.append_clean(item.to_org())
        base.root.append_clean(orgProject)

    base.save_to_file(filename)


def upload(filename):
    base = PyOrgMode.OrgDataStructure()
    base.load_from_file(filename)

    orgItems = items.from_org(base.root.content)
    doneItems = (x for x in orgItems if x.done)

    api.items.complete([x.id for x in doneItems])
    api.commit()
