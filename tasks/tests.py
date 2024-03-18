from django.test import TestCase
from .models import Task

# Create your tests here.
# Create tests for tasks views
def test_task_list_view(self):
    response = self.client.get('/tasks/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Tasks')
    self.assertTemplateUsed(response, 'tasks/task_list.html')

def test_task_detail_view(self):
    response = self.client.get('/tasks/1/')
    no_response = self.client.get('/tasks/100000/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(no_response.status_code, 404)
    self.assertContains(response, 'Task')
    self.assertTemplateUsed(response, 'tasks/task_detail.html')

def test_task_create_view(self):
    response = self.client.post('/tasks/new/', {
        'assigned_to': 1,
        'title': 'New task',
        'description': 'New task description',
        'priority': 'Low',
        'due_date': '2021-12-12'
    })
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Task.objects.last().title, 'New task')
    self.assertEqual(Task.objects.last().description, 'New task description')
    self.assertEqual(Task.objects.last().priority, 'Low')
    self.assertEqual(Task.objects.last().due_date, '2021-12-12')

def test_task_update_view(self):
    response = self.client.post('/tasks/1/update/', {
        'status': 'Completed'
    })
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Task.objects.get(id=1).status, 'Completed')

def test_task_delete_view(self):
    response = self.client.post('/tasks/1/delete/')
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Task.objects.filter(id=1).count(), 0)


