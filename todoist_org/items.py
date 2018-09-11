from bidict import bidict
from dateparser import parse as dateparse
from PyOrgMode import PyOrgMode


class Item:
    priority_dict = bidict({1: '', 2: 'C', 3: 'B', 4: 'A'})

    def __init__(self,
                 project_id,
                 item_id,
                 description,
                 priority,
                 done,
                 due_date=None):
        self.project_id = int(project_id)
        self.id = int(item_id)
        self.description = description
        self.priority = priority
        self.done = done
        self.due_date = None if (due_date is None) else dateparse(due_date)

    @classmethod
    def from_todoist(cls, todoist_item):
        return cls(todoist_item['project_id'], todoist_item['id'],
                   todoist_item['content'], todoist_item['priority'],
                   todoist_item['checked'] == 1, todoist_item['due_date_utc'])

    @classmethod
    def from_org(cls, org_item):
        return cls(
            cls.get_org_prop(org_item.parent, 'ID'),
            cls.get_org_prop(org_item, 'ID'), org_item.heading,
            cls.priority_dict.inv[org_item.priority], org_item.todo == 'DONE')

    def to_org(self):
        elem = PyOrgMode.OrgNode.Element()
        elem.level = 2
        elem.heading = self.description
        elem.priority = self.priority_dict[self.priority]
        elem.todo = 'DONE' if self.done else 'TODO'

        props = PyOrgMode.OrgDrawer.Element('PROPERTIES')
        props.append(PyOrgMode.OrgDrawer.Property('ID', f"{self.id}"))
        elem.append_clean(props)

        if self.due_date is not None:
            formatted_date = self.due_date.astimezone().strftime(
                '<%Y-%m-%d %a %H:%M>')
            sched = PyOrgMode.OrgSchedule()
            sched._append(elem, sched.Element(deadline=formatted_date))

        return elem

    @staticmethod
    def get_org_prop(org_item, prop_name):
        properties = next(
            x for x in org_item.content
            if isinstance(x, PyOrgMode.OrgDrawer.Element)
            and x.name == 'PROPERTIES').content

        return next(x.value for x in properties if x.name == prop_name)


def from_todoist(todoist_items):
    return (Item.from_todoist(x) for x in todoist_items)


def from_org(org_projects):
    items = []
    for project in org_projects:
        for item in project.content:
            if isinstance(item, PyOrgMode.OrgNode.Element):
                items.append(Item.from_org(item))
    return items
