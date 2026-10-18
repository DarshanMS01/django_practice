from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from employees.models import employee


class EmailLoginTests(TestCase):
    def setUp(self):
        self.password = 'S3curePass!xyz'
        self.user = User.objects.create_user(
            username='darshan',
            email='darshan@example.com',
            password=self.password,
        )

    def test_home_page_public(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Employee Records - Tech With Darshan')
        self.assertContains(response, 'Add Employee')
        self.assertContains(response, 'Login')

    def test_valid_email_login(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'darshan@example.com', 'password': self.password},
        )
        self.assertRedirects(response, reverse('home'))
        self.assertTrue('_auth_user_id' in self.client.session)

        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Welcome, darshan')
        self.assertContains(response, 'Logout')
        self.assertNotContains(response, '>Login</a>')

    def test_email_login_case_insensitive(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'Darshan@Example.COM', 'password': self.password},
        )
        self.assertRedirects(response, reverse('home'))

    def test_invalid_password_login(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'darshan@example.com', 'password': 'wrong-password'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_unknown_email_login(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'nobody@example.com', 'password': self.password},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_login_does_not_create_users(self):
        before = User.objects.count()
        self.client.post(
            reverse('login'),
            {'email': 'ghost@example.com', 'password': 'whatever123'},
        )
        self.assertEqual(User.objects.count(), before)

    def test_session_persists_across_requests(self):
        self.client.post(
            reverse('login'),
            {'email': 'darshan@example.com', 'password': self.password},
        )
        for _ in range(3):
            response = self.client.get(reverse('home'))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['user'].is_authenticated)

    def test_logout_post(self):
        self.client.post(
            reverse('login'),
            {'email': 'darshan@example.com', 'password': self.password},
        )
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)

        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Login')

    def test_logout_get_does_not_log_out(self):
        self.client.post(
            reverse('login'),
            {'email': 'darshan@example.com', 'password': self.password},
        )
        self.client.get(reverse('logout'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_username_backend_still_works(self):
        # Admin (username-based) login must keep working.
        from django.contrib.auth import authenticate
        user = authenticate(username='darshan', password=self.password)
        self.assertIsNotNone(user)


class ProtectedEmployeeViewsTests(TestCase):
    def setUp(self):
        self.password = 'S3curePass!xyz'
        self.user = User.objects.create_user(
            username='darshan',
            email='darshan@example.com',
            password=self.password,
        )

    def test_add_employee_anonymous_redirects_to_login(self):
        response = self.client.get(reverse('add_employee'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('add_employee')}",
        )

    def test_add_employee_post_anonymous_redirects(self):
        response = self.client.post(reverse('add_employee'), {})
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('add_employee')}",
        )
        self.assertEqual(employee.objects.count(), 0)

    def test_add_employee_logged_in_get(self):
        self.client.login(email='darshan@example.com', password=self.password)
        response = self.client.get(reverse('add_employee'))
        self.assertEqual(response.status_code, 200)

    def test_add_employee_logged_in_post_creates(self):
        self.client.login(email='darshan@example.com', password=self.password)
        response = self.client.post(
            reverse('add_employee'),
            {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'jane@example.com',
                'salary': '50000',
                'designation': 'Engineer',
                'joining_date': date.today().isoformat(),
                'is_active': 'on',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(employee.objects.filter(email='jane@example.com').exists())

    def test_employee_detail_stays_public(self):
        emp = employee.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            salary=50000,
            designation='Engineer',
            joining_date=date.today(),
        )
        response = self.client.get(reverse('employee_detail', args=[emp.id]))
        self.assertEqual(response.status_code, 200)


class RegistrationTests(TestCase):
    def test_register_with_email_then_login(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'email': 'new@example.com',
                'password1': 'Tr0ub4dor&3xyz',
                'password2': 'Tr0ub4dor&3xyz',
            },
        )
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

        response = self.client.post(
            reverse('login'),
            {'email': 'new@example.com', 'password': 'Tr0ub4dor&3xyz'},
        )
        self.assertRedirects(response, reverse('home'))
