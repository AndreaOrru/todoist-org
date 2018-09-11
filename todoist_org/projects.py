from PyOrgMode import PyOrgMode


class Project:
    def __init__(self, project_id, project_name):
        self.id = project_id
        self.name = project_name

    @classmethod
    def from_todoist(cls, todoist_item):
        return cls(todoist_item['id'], todoist_item['name'])

    def to_org(self):
        elem = PyOrgMode.OrgNode.Element()
        elem.level = 1
        elem.heading = self.name

        props = PyOrgMode.OrgDrawer.Element('PROPERTIES')
        props.append(PyOrgMode.OrgDrawer.Property('ID', f"{self.id}"))
        elem.append_clean(props)

        return elem


def from_todoist(todoist_projects):
    return (Project.from_todoist(x) for x in todoist_projects)
