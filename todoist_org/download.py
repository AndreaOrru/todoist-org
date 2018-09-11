def remote_to_local(filename):
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
