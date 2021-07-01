from scraping.utils import post_request_json, write_html, get_request_json, write_excel
from datetime import datetime

data_header = [
    ['Main Unit', 'Sub Unit', 'Assignee', 'Link To SME Doc', 'Link To Story Doc', 'Prod house', 'Prod brief date']]
token = 'b47630c0391ac90'
base_url = 'https://app.clickup.com/v1/public/view/4-16817591-1'


def get_tasks():
    url = base_url + '?token=' + token
    json_obj = get_request_json(url, '')
    task_groups = json_obj['list']['groups']

    task_id_list = []
    for task in task_groups:
        task_id_list += task['task_ids']
    return task_id_list


def get_task_info(task_id_list):
    print('start-task, size=', len(task_id_list))
    url = base_url + '/tasks'

    request_body = {
        "show_closed_subtasks": True,
        "rollup": [],
        "task_ids": task_id_list,
        "fields": ["assignees", "assigned_comments_count", "assigned_checklist_items", "dependency_state",
                   "parent_task", "attachments_count", "followers", "totalTimeSpent", "subtasks_count",
                   "subtasks_by_status", "tags", "simple_statuses", "customFields", "fallback_coverimage",
                   "attachments_thumbnail_count", "rolledUpTimeSpent", "rolledUpTimeEstimate", "rolledUpPointsEstimate",
                   "linkedTasks", "docs_count", "pullRequests", "incompleteCommentCount", "statuses", "latestComment",
                   "comment_count", "current_status", "status_history"],
        "include_default_permissions": False,
        "token": token
    }

    res_obj = post_request_json(url, '', request_body)
    tasks = res_obj['tasks']
    for task in tasks:
        main_unit_name = task['name']
        task_id = task['id']
        get_sub_task_info(task_id, main_unit_name)


def get_sub_task_info(task_id, main_unit_name):
    url = base_url + '/tasks'
    prod_house_dict = {
        0: 'GS',
        1: 'RS',
        2: 'TT',
        3: 'AM',
        4: 'RC',
        -1: 'N/A',
    }
    request_body = {"team_id": "10587447", "parent": task_id,
                    "order": "{\"field\":\"items.subtask_orderindex\",\"dir\":\"asc\"}", "archived": "true",
                    "include_closed": True, "immediate_children": True, "task_ids": [],
                    "fields": ["assignees", "assigned_comments_count", "assigned_checklist_items", "dependency_state",
                               "parent_task", "attachments_count", "followers", "totalTimeSpent", "subtasks_count",
                               "subtasks_by_status", "tags", "simple_statuses", "customFields", "fallback_coverimage",
                               "attachments_thumbnail_count", "rolledUpTimeSpent", "rolledUpTimeEstimate",
                               "rolledUpPointsEstimate", "linkedTasks", "docs_count", "pullRequests",
                               "incompleteCommentCount"], "include_default_permissions": False,
                    "token": token}
    res_obj = post_request_json(url, '', request_body)
    tasks = res_obj['tasks']
    for task in tasks:
        sub_main_unit = task['name']
        assignees_list = task['assignees']
        assignees = ''
        for a in assignees_list:
            assignees = assignees + '|' + a['username']
        if not assignees:
            assignees = '|N/A'
        customFields = task['customFields']
        link_sme = 'N/A'
        link_story = 'N/A'
        prod_house = 'N/A'
        video_sent = 'N/A'
        for c in customFields:
            if c['sort_col'] == 'Link to SME DOC':
                link_sme = c.get('value', 'N/A')
            if c['sort_col'] == 'Link to Story Doc':
                link_story = c.get('value', 'N/A')
            if c['sort_col'] == 'Production house':
                prod_house = prod_house_dict.get(c.get('value', -1), 'N/A')
            if 'Video brief sent' in c['sort_col']:
                video_sent = get_date_from_timestamp(c.get('value'))
        one_row = [main_unit_name, sub_main_unit, assignees[1:], link_sme, link_story, prod_house, video_sent]
        data_header.append(one_row)


def get_date_from_timestamp(timestamp):
    try:
        return datetime.utcfromtimestamp(int(timestamp)/1000).strftime('%d/%m/%Y')
    except:
        return 'N/A'


def store_file():
    filename = datetime.now().strftime('%d-%m-%Y') + '.xls'
    write_excel(filename, data_header)

# task_ids = get_tasks()
# get_task_info(task_ids)
store_file()