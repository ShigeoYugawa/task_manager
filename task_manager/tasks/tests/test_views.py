# task_manager/tasks/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from tasks.models import Task

class TaskViewsTestCase(TestCase):
    def setUp(self):
        # テスト用タスクを作成
        self.task1 = Task.objects.create(title="Python学習", is_completed=False, is_archived=False)
        self.task2 = Task.objects.create(title="Django復習", is_completed=True, is_archived=False)
        self.task3 = Task.objects.create(title="API設計", is_completed=False, is_archived=True)

    def test_task_list_view_status_code(self):
        url = reverse('tasks:task_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertIn(self.task1, response.context['tasks'])
        self.assertIn(self.task2, response.context['tasks'])
        self.assertIn(self.task3, response.context['tasks'])

    def test_task_list_view_filter_completed(self):
        url = reverse('tasks:task_list') + '?is_completed=true'
        response = self.client.get(url)
        tasks = response.context['tasks']
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.task1, tasks)
        self.assertNotIn(self.task3, tasks)

    def test_task_list_view_filter_archived(self):
        url = reverse('tasks:task_list') + '?is_archived=true'
        response = self.client.get(url)
        tasks = response.context['tasks']
        self.assertIn(self.task3, tasks)
        self.assertNotIn(self.task1, tasks)
        self.assertNotIn(self.task2, tasks)

    def test_task_list_view_search_query(self):
        url = reverse('tasks:task_list') + '?q=Python'
        response = self.client.get(url)
        tasks = response.context['tasks']
        self.assertIn(self.task1, tasks)
        self.assertNotIn(self.task2, tasks)
        self.assertNotIn(self.task3, tasks)

    def test_task_detail_view(self):
        url = reverse('tasks:task_detail', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertEqual(response.context['task'], self.task1)

    def test_task_create_view_get(self):
        url = reverse('tasks:task_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

    def test_task_create_view_post(self):
        url = reverse('tasks:task_create')
        data = {'title': '新規タスク', 'is_completed': False, 'is_archived': False}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='新規タスク').exists())

    def test_task_update_view_get(self):
        url = reverse('tasks:task_update', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

    def test_task_update_view_post(self):
        url = reverse('tasks:task_update', args=[self.task1.pk])
        data = {'title': '更新済みタスク', 'is_completed': True, 'is_archived': False}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, '更新済みタスク')
        self.assertTrue(self.task1.is_completed)

    def test_task_delete_view_get(self):
        url = reverse('tasks:task_delete', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')

    def test_task_delete_view_post(self):
        url = reverse('tasks:task_delete', args=[self.task1.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
