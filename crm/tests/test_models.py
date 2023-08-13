from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from crm.models import Chicken, Egg

class ChickenModelTest(TestCase):

    # Set up a user and a chicken object
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.chicken = Chicken.objects.create(
            date_added=timezone.now(),
            age=10,
            health_status=0,
            purpose=0,
            owner=self.user
        )
    
    # Test that the chicken model is created correctly
    def test_create_chicken_model(self):
        self.assertEqual(self.chicken.age, 10)
        self.assertEqual(self.chicken.health_status, 0)
        self.assertEqual(self.chicken.purpose, 0)
        self.assertEqual(self.chicken.owner, self.user)

class EggModelTest(TestCase):

    # Set up a user and an egg object
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.egg = Egg.objects.create(
            collection_date=timezone.now().date(),
            quantity=10,
            size=0,
            owner=self.user
        )

    # Test that the egg model is created correctly
    def test_create_egg_model(self):
        self.assertEqual(self.egg.collection_date, timezone.now().date())
        self.assertEqual(self.egg.quantity, 10)
        self.assertEqual(self.egg.size, 0)
        self.assertEqual(self.egg.owner, self.user)