from django.test import TestCase
from django.contrib.auth.models import User, Group


class AdminAccessTests(TestCase):
    def setUp(self):
        # create admin user and site admin group
        self.username = 'admin_test'
        self.password = 'testpass'
        u = User.objects.create_user(self.username, 'admin@example.com', self.password)
        g, _ = Group.objects.get_or_create(name='SiteAdmin')
        g.user_set.add(u)

        # create a normal user
        self.user = User.objects.create_user('normal', 'n@example.com', 'pw')

    def test_admin_dashboard_access(self):
        # login as admin_test
        logged = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged, 'Admin test user should be able to login')
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Admin Dashboard')

    def test_non_admin_cannot_access(self):
        self.client.login(username='normal', password='pw')
        resp = self.client.get('/admin/')
        # non-admin should be redirected to login or denied
        self.assertNotEqual(resp.status_code, 200)
