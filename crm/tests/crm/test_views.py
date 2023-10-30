from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from crm.models import Egg, Chicken
from crm.forms import SignUpForm, AddEggForm, AddChickenForm
from crm.views import IndexView, EggView


class IndexViewTest(TestCase):
    pass


class EggViewTest(TestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user.save()

        # eggs created uses different date to distinguish them
        collection_date = timezone.now().date()
        number_of_eggs = 5
        for egg in range(number_of_eggs):
            Egg.objects.create(
                collection_date=collection_date - timedelta(days=egg),
                size=0,
                owner=self.user,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("crm:egg_view", kwargs={"pk": 1}))
        self.assertRedirects(response, "/")

    def test_logged_in_url_exist_and_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("crm:egg_view", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/egg/view.html")

    def test_no_egg_record(self):
        Egg.objects.all().delete()
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("crm:egg_view", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anda tidak mempunyai rekod telur")

    def test_egg_record_exist(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("crm:egg_view", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["egg_list"]), 5)

    def test_egg_record_exist_not_belonged_to_user(self):
        self.user2 = User.objects.create_user(username="testuser2", password="testpass")
        self.client.login(username="testuser2", password="testpass")
        response = self.client.get(reverse("crm:egg_view", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/egg/all/{}/".format(self.user2.id))


class EggAddTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("crm:egg_add"))
        self.assertRedirects(response, "/")

    def test_logged_in_url_exist_and_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("crm:egg_add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/egg/add.html")

    def test_egg_add_form_instance(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("crm:egg_add"))
        self.assertIsInstance(response.context["form"], AddEggForm)

    def test_egg_add_form_valid(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("crm:egg_add"),
            {
                "size0": ["Kecil"],
                "quantity0": [""],
                "size1": ["Sederhana"],
                "quantity1": ["2"],
                "size2": ["Besar"],
                "quantity2": [""],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("crm:egg_view", kwargs={"pk": 1}))

    def test_egg_add_form_invalid(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("crm:egg_add"),
            {
                "size0": ["Kecil"],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("crm:egg_add"))


class EggUpdateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user.save()

        for num_of_egg in range(3):
            for egg in range(num_of_egg + 1):
                Egg.objects.create(
                    collection_date=timezone.now().date(), size=egg, owner=self.user
                )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("crm:egg_update", kwargs={"date": timezone.now().date()})
        )
        self.assertRedirects(response, "/")

    def test_logged_in_url_exist_and_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("crm:egg_update", kwargs={"date": timezone.now().date()})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/egg/update.html")

    def test_egg_update_valid_form(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("crm:egg_update", kwargs={"date": timezone.now().date()}),
            {
                "size0": ["Kecil"],
                "quantity0": ["3"],
                "size1": ["Sederhana"],
                "quantity1": ["1"],
                "size2": ["Besar"],
                "quantity2": ["4"],
            },
        )
        # self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("crm:egg_detail", kwargs={"date": timezone.now().date()})
        )
        self.assertEqual(len(Egg.objects.all()), 8)

    def test_egg_update_invalid_form(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("crm:egg_update", kwargs={"date": timezone.now().date()}),
            {
                "size0": ["Kecil"],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("crm:egg_update", kwargs={"date": timezone.now().date()})
        )
        # self.assertEqual(len(Egg.objects.all()), 6)


class EggDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user.save()

        self.egg = Egg.objects.create(
            collection_date=timezone.now().date(), size=0, owner=self.user
        )

    def test_delete_successful(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("crm:egg_delete", kwargs={"date": self.egg.collection_date})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("crm:egg_view", kwargs={"pk": self.user.id})
        )
        # Verify that the egg record has been deleted
        egg_exists = Egg.objects.filter(
            collection_date=self.egg.collection_date
        ).exists()
        self.assertFalse(egg_exists)
