from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from collections import defaultdict
from crm.models import Egg, Chicken
from crm.forms import SignUpForm, AddEggForm, UpdateEggForm, AddChickenForm
from crm.views import index, logout_view, register_view, egg_view, add_egg_view, update_egg_view, delete_egg_view, add_chicken_view, delete_chicken_view, chicken_view, update_chicken_view

class IndexViewTest(TestCase):
    def test_index_view_with_no_user(self):
        """
        If no user, display the index page with login form
        """
        response = self.client.get(reverse('crm:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log Masuk")
    
    def test_index_view_existed_at_desired_location(self):
        response = self.client.get('/crm/')
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('crm:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/index.html')

    def test_index_view_with_invalid_user(self):
        """
        If invalid user, display the index page with error message
        """
        response = self.client.post(reverse('crm:index'), {'username': 'invalid', 'password': 'invalid'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('crm:index'))
        self.assertContains(response, "Kata Laluan atau/dan Nama Pengguna tidak sah")

    def test_index_view_with_valid_user(self):
        """
        If valid user, display the index page with success message
        """
        user = User.objects.create_user(username='testuser', password='12345@th8j')
        response = self.client.post(reverse('crm:index'), user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('crm:index'))
        self.assertContains(response, "Selamat Datang")

class LogoutViewTest(TestCase):

    def test_logout_view(self):
        """
        logout view redirects to index page
        """
        response = self.client.get(reverse('crm:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('crm:index'))
        self.assertContains(response, "Log Keluar berjaya")

class RegisterViewTest(TestCase):

    def test_register_view_with_invalid_form(self):
        """
        If invalid form, display the register page with error message
        """
        response = self.client.post(reverse('crm:register'), {'username': 'invalid', 'email': 'invalid', 'password1': 'invalid', 'password2': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/register.html')
        self.assertContains(response, "Sila betulkan ralat di bawah")

    def test_register_view_with_valid_form(self):
        """
        If valid form, redirect to index page with success message
        """
        response = self.client.post(reverse('crm:register'), {'username': 'testuser', 'email': 'test@gmail.com', 'password1': 'pass823@h', 'password2': 'pass823@h'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('crm:index'))
        self.assertContains(response, "Pendaftaran berjaya. Sila log masuk")

class EggViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345@th8j')
        self.client.login(username='testuser', password='12345@th8j')
        self.egg = Egg.objects.create(user=self.user, date=timezone.now().date(), quantity=10, size=1)
        self.url = reverse('crm:egg_view', args=[self.user.id])

    def test_egg_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/egg_view.html')

    def test_egg_view_with_permisson(self):
        """
        If user has permission, display the egg page
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_egg_view_with_no_permisson(self):
        """
        If user has no permission, display the egg page with error message
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('crm:index'))
        self.assertContains(response, "Sila log masuk")

    def test_egg_view_no_egg_record(self):
        Egg.objects.filter(owner=self.user).delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_egg_view_existing_egg_records(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, timezone.now().date())
        self.assertContains(response, 10)

class AddEggViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345@th8j')
        self.client.login(username='testuser', password='12345@th8j')
        self.url = reverse('crm:egg_add', args=[])

        for i in range(1, 3):
            Egg.objects.create(user=self.user, date=timezone.now().date(), quantity=i-1, size=1)
    
    # test add_egg_view_existed_at_desired_location
    def test_add_egg_existed_at_desired_location(self):
        response = self.client.get('/crm/egg/add_egg/')
        self.assertEqual(response.status_code, 200)

    


    
        
