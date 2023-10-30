from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from crm.models import Chicken, Egg, EggShipment

class ChickenModelTest(TestCase):

    # Set up a user and a chicken object
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.chicken = Chicken.objects.create(
            date_added=timezone.now().date(),
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

    def test_chicken_model_str_method(self):
        self.assertEqual(str(self.chicken), '10 week old chicken, Sihat on testuser\'s farm')

    def test_chicken_model_get_health_status_display_method(self):
        self.assertEqual(self.chicken.get_health_status_display(), 'Sihat')

    def test_chicken_model_get_purpose_display_method(self):
        self.assertEqual(self.chicken.get_purpose_display(), 'Petelur')

    def test_chicken_model_get_age_method(self):
        self.assertEqual(self.chicken.get_age(), 10)

class EggModelTest(TestCase):

    # Set up a user and an egg object
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.egg_shipment = EggShipment.objects.create(
            date_shipped=timezone.now().date(),
            customer='testcustomer',
            owner=self.user
        )
        self.egg = Egg.objects.create(
            collection_date=timezone.now().date(),
            size=0,
            owner=self.user,
            egg_shipment=self.egg_shipment
        )

    # Test that the egg model is created correctly
    def test_create_egg_model(self):
        self.assertEqual(self.egg.collection_date, timezone.now().date())
        self.assertEqual(self.egg.size, 0)
        self.assertEqual(self.egg.owner, self.user)
        self.assertEqual(self.egg.egg_shipment, self.egg_shipment)

    def test_egg_model_str_method(self):
        self.assertEqual(str(self.egg), 'Telur saiz Kecil dikutip pada {}'.format(timezone.now().date()))

    def test_egg_model_get_size_display_method(self):
        self.assertEqual(self.egg.get_size_display(), 'Kecil')

class EggShipmentModelTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )

        self.egg_shipment = EggShipment.objects.create(
            date_shipped=timezone.now().date(),
            customer = 'testcustomer',
            owner = self.user
        )
        for j in range(2):
            for i in range(12):
                    Egg.objects.create(
                        collection_date = timezone.now().date(),
                        size = j,
                        owner = self.user,
                        egg_shipment = self.egg_shipment
                    )

    def test_create_egg_shipment_model(self):
        self.assertEqual(self.egg_shipment.date_shipped, timezone.now().date())
        self.assertEqual(self.egg_shipment.customer, 'testcustomer')
        self.assertEqual(self.egg_shipment.owner, self.user)

    def test_egg_shipment_model_str_method(self):
        self.assertEqual(str(self.egg_shipment), 'testcustomer - {} - 2 dozens'.format(timezone.now().date()))

    def test_egg_shipment_model_get_total_dozens_method(self):
        self.assertEqual(self.egg_shipment.get_total_dozens(), 2)

    def test_egg_shipment_model_get_eggs_counts_by_size_method(self):
        self.assertEqual(self.egg_shipment.get_eggs_counts_by_size(), {'small': '12 telur kecil', 'medium': '12 telur sederhana'})

    def test_egg_shipment_model_get_total_sales_method(self):
        self.assertEqual(self.egg_shipment.get_total_sales(), 12.0)