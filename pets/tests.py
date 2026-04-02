from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from .models import Pet

User = get_user_model()


class PetModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123!',
            user_type='owner'
        )
        self.pet = Pet.objects.create(
            owner=self.user,
            name='Max',
            species='dog',
            date_of_birth=date(2020, 5, 15)
        )

    def test_pet_str(self):
        self.assertEqual(str(self.pet), 'Max (testuser)')

    def test_pet_age(self):
        expected_age = date.today().year - 2020
        self.assertIn(self.pet.age, [expected_age, expected_age - 1])


class PetListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123!',
            user_type='owner'
        )
        self.pet_list_url = reverse('pets:pet_list')

    def test_pet_list_requires_login(self):
        response = self.client.get(self.pet_list_url)
        self.assertEqual(response.status_code, 302)

    def test_pet_list_shows_only_own_pets(self):
        Pet.objects.create(
            owner=self.user,
            name='Max',
            species='dog',
            date_of_birth=date(2020, 1, 1)
        )

        other_user = User.objects.create_user(
            username='other',
            password='TestPass123!'
        )
        Pet.objects.create(
            owner=other_user,
            name='Luna',
            species='cat',
            date_of_birth=date(2021, 1, 1)
        )

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(self.pet_list_url)

        self.assertContains(response, 'Max')
        self.assertNotContains(response, 'Luna')


class PetCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123!',
            user_type='owner'
        )
        self.client.login(username='testuser', password='TestPass123!')
        self.pet_create_url = reverse('pets:pet_create')

    def test_pet_create_page_loads(self):
        response = self.client.get(self.pet_create_url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_pet(self):
        data = {
            'name': 'Buddy',
            'species': 'dog',
            'date_of_birth': '2022-01-15',
        }
        response = self.client.post(self.pet_create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pet.objects.filter(name='Buddy').exists())

    def test_created_pet_belongs_to_user(self):
        data = {
            'name': 'Charlie',
            'species': 'cat',
            'date_of_birth': '2023-03-20',
        }
        self.client.post(self.pet_create_url, data)
        pet = Pet.objects.get(name='Charlie')
        self.assertEqual(pet.owner, self.user)
