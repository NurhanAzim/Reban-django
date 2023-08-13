from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from crm.forms import SignUpForm, AddEggForm, UpdateEggForm, AddChickenForm
from crm.models import Chicken, Egg

class SignUpFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
        )
        self.user.set_password('123w456dawd78')
        self.user.save()


    # test SignUpForm has all fields
    def test_sigup_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    # test SignUpForm email entered not valid
    def test_signup_form_email_not_valid(self):
        form = SignUpForm()
        self.assertFalse(form.fields['email'].validators[0]('test'))

    # test SignUpForm email entered valid
    def test_signup_form_email_valid(self):
        form = SignUpForm()
        self.assertTrue(form.fields['email'].validators[0]('testuser@gmail.com'))

    # test SignUpForm username entered not valid
    def test_signup_form_username_not_valid(self):
        form = SignUpForm()
        self.assertFalse(form.fields['username'].validators[0]('testuser'))
        self.assertFalse(form.fields['username'].validators[0]('a'*151))
        self.assertFalse(form.fields['username'].validators[0]('test$'))
        self.assertFalse(form.fields['username'].validators[0](12345))

    # test SignUpForm username entered valid
    def test_signup_form_username_valid(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].validators[0]('test_user'), None)
        self.assertEqual(form.fields['username'].validators[0]('a'*150), None)
        self.assertEqual(form.fields['username'].validators[0]('test_user123'), None)
        self.assertEqual(form.fields['username'].validators[0]('test_user-123@+'), None)

    # test SignUpForm password1 entered not valid
    def test_signup_form_password1_not_valid(self):
        form = SignUpForm()
        self.assertFalse(form.fields['password1'].validators[0]('12345'))
        self.assertFalse(form.fields['password1'].validators[0]('a'*7))
        self.assertFalse(form.fields['password1'].validators[0]('testuser'))

    # test SignUpForm password1 entered valid
    def test_signup_form_password1_valid(self):
        form = SignUpForm()
        self.assertEqual(form.fields['password1'].validators[0]('123w456dawd78'), None)
        self.assertEqual(form.fields['password1'].validators[0]('testuser123'), None)

    # test SignUpForm password2 entered not valid
    def test_signup_form_password2_not_valid(self):
        form = SignUpForm()
        self.assertFalse(form.fields['password2'].validators[0]('12345'))
    
    # test SignUpForm password2 entered valid
    def test_signup_form_password2_valid(self):
        form = SignUpForm()
        self.assertEqual(form.fields['password2'].validators[0]('123w456dawd78'), None)

    # test SignUpForm save
    def test_signup_form_save(self):
        
        form = SignUpForm(data={
            'username': 'nohan',
            'email': 'testuser@gmail.com',
            'password1': '123w456dawd78',
            'password2': '123w456dawd78',
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(get_user_model().objects.all().count(), 2)
    
    # test SignUpForm save fail
    def test_signup_form_save_fail(self):
        form = SignUpForm(data={
            'username': 'testuser1',
            'email': 'testuser@yahoo.com',
            'password1': '123w456dawd78',
            'password2': '123w456dawd78',
        })
        self.assertFalse(form.is_valid())
        form.save()
        self.assertEqual(get_user_model().objects.all().count(), 1)

class AddEggFormTest(TestCase):
    # test AddEggForm has all fields
    def test_add_egg_form_has_fields(self):
        form = AddEggForm()
        expected = ['quantity', 'size']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


    # test AddEggForm size entered not valid
    def test_add_egg_form_size_not_valid(self):
        form = AddEggForm()
        self.assertFalse(form.fields['size'].validators[0](-1))
        self.assertFalse(form.fields['size'].validators[0](10))

    # test AddEggForm size entered valid
    def Test_add_egg_form_size_valid(self):
        form = AddEggForm()
        self.assertEqual(form.fields['size'].validators[0][0], None)

    # test AddEggForm quantity entered not valid
    def test_add_egg_form_quantity_not_valid(self):
        form = AddEggForm()
        self.assertFalse(form.fields['quantity'].validators[0][-1])
        self.assertFalse(form.fields['quantity'].validators[0][0])
    
    # test AddEggForm quantity entered valid
    def test_add_egg_form_quantity_valid(self):
        form = AddEggForm()
        self.assertEqual(form.fields['quantity'].validators[0][0], None)

    # test AddEggForm save
    def test_add_egg_form_save(self):
        form = AddEggForm(data={
            'size': 0,
            'quantity': 10,
            'collection_date': '2023-08-09',
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Egg.objects.all().count(), 1)

    # test AddEggForm save fail
    def test_add_egg_form_save_fail(self):
        form = AddEggForm(data={
            'size': 10,
            'quantity': 10,
            'collection_date': '2023-08-09',
        })
        self.assertFalse(form.is_valid())
        form.save()
        self.assertEqual(Egg.objects.all().count(), 0)

class UpdateEggFormTest(TestCase):
    
    def test_update_egg_form_has_fields(self):
        form = UpdateEggForm()
        expected = ['quantity']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


    # test UpdateEggForm size entered not valid
    def test_update_egg_form_size_not_valid(self):
        form = UpdateEggForm()
        self.assertFalse(form.fields['size'].validators[0](-1))
        self.assertFalse(form.fields['size'].validators[0](10))

    # test UpdateEggForm size entered valid
    def Test_update_egg_form_size_valid(self):
        form = UpdateEggForm()
        self.assertEqual(form.fields['size'].validators[0][0], None)

    # test UpdateEggForm quantity entered not valid
    def test_update_egg_form_quantity_not_valid(self):
        form = UpdateEggForm()
        self.assertFalse(form.fields['quantity'].validators[0][-1])
        self.assertFalse(form.fields['quantity'].validators[0][0])

    # test UpdateEggForm quantity entered valid
    def test_update_egg_form_quantity_valid(self):
        form = UpdateEggForm()
        self.assertEqual(form.fields['quantity'].validators[0][0], 0)


    # test UpdateEggForm save
    def test_update_egg_form_save(self):
        form = UpdateEggForm(data={
            'size': 0,
            'quantity': 10,
            'collection_date': '2023-08-09'
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Egg.objects.all().count(), 1)

    # test UpdateEggForm save fail
    def test_update_egg_form_save_fail(self):
        form = UpdateEggForm(data={
            'size': 'test',
            'quantity': 10,
        })
        self.assertFalse(form.is_valid())
        form.save()
        self.assertEqual(Egg.objects.all().count(), 0)

class AddChickenFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='123w456dawd78',
        )
    
    #test AddChickenForm has all fields
    def test_add_chicken_form_has_fields(self):
        form = AddChickenForm()
        expected = ['date_added', 'age', 'health_status', 'purpose']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    # test AddChickenForm choices are correct
    def test_add_chicken_form_choices(self):
        form = AddChickenForm()
        self.assertEqual(form.fields['purpose'].choices, [(0, 'Petelur'), (1, 'Pedaging')])
        self.assertEqual(form.fields['health_status'].choices, [(0, 'Sihat'), (1, 'Sakit')])

    # test AddChickenForm date_added in the past should return true
    def test_add_chicken_form_date_added_in_the_past(self):
        date = timezone.now().date() - datetime.timedelta(days=1)
        form = AddChickenForm(data={'date_added': date, 'age': 10, 'health_status': 0, 'purpose': 0})
        self.assertTrue(form.is_valid())

    # test AddChickenForm date_added in the future should return false
    def test_add_chicken_form_date_added_in_the_future(self):
        date = timezone.now().date() + datetime.timedelta(days=1)
        form = AddChickenForm(data={'date_added': date, 'age': 10, 'health_status': 0, 'purpose': 0})
        self.assertFalse(form.is_valid())

    #test AddChickenForm date_added today should return true
    def test_add_chicken_form_date_added_today(self):
        date = datetime.date.today()
        form = AddChickenForm(data={'date_added': date, 'age': 10, 'health_status': 0, 'purpose': 0})
        self.assertTrue(form.is_valid())

    # test AddChickenForm age entered not valid
    def test_add_chicken_form_age_not_valid(self):
        form = AddChickenForm()
        self.assertFalse(form.fields['age'].validators[0][-1])
        self.assertFalse(form.fields['age'].validators[0][0])
    
    # test AddChickenForm age entered valid
    def test_add_chicken_form_age_valid(self):
        form = AddChickenForm()
        self.assertEqual(form.fields['age'].validators[0][1], True)
    
    # test AddChickenForm health_status entered not valid
    def test_add_chicken_form_health_status_not_valid(self):
        form = AddChickenForm()
        self.assertFalse(form.fields['health_status'].validators[0][-1])
        self.assertFalse(form.fields['health_status'].validators[0][2])

    # test AddChickenForm health_status entered valid
    def test_add_chicken_form_health_status_valid(self):
        form = AddChickenForm()
        self.assertTrue(form.fields['health_status'].validators[0][1])

    # test AddChickenForm purpose entered not valid
    def test_add_chicken_form_purpose_not_valid(self):
        form = AddChickenForm()
        self.assertFalse(form.fields['purpose'].validators[0][-1])
        self.assertFalse(form.fields['purpose'].validators[0][2])

    # test AddChickenForm purpose entered valid
    def test_add_chicken_form_purpose_valid(self):
        form = AddChickenForm()
        self.assertEqual(form.fields['purpose'].validators[0][0], None)

    # test AddChickenForm save
    def test_add_chicken_form_save(self):
        form = AddChickenForm(data={
            'date_added': datetime.date.today(),
            'age': 10,
            'health_status': 0,
            'purpose': 0,
            'owner': self.user
        })
        self.assertTrue(form.is_valid())
        if form.is_valid():
            form.save()
        self.assertEqual(Chicken.objects.all().count(), 1)
    
    # test AddChickenForm save fail
    def test_add_chicken_form_save_fail(self):
        form = AddChickenForm(data={
            'date_added': datetime.date.today(),
            'age': 10,
            'health_status': 0,
            'purpose': 10,
        })
        self.assertFalse(form.is_valid())
        if form.is_valid():
            form.save()
        self.assertEqual(Chicken.objects.all().count(), 0)

