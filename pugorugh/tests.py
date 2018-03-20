from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Dog, UserDog, UserPref


class TestDogModel(TestCase):
    def setUp(self):
        Dog.objects.create(
            name='max',
            image_filename='maxpic',
            breed='dachsund',
            age=8
        )

    def test_dog_creation(self):
        dog = Dog.objects.get(name='max')
        self.assertEqual('max', dog.name)


class TestUserPrefModel(TestCase):
    def setUp(self):
        self.taylor = User.objects.create(
            username='taylor',
            password='taylor'
        )
        self.userprefs = UserPref.objects.create(user=self.taylor)

    def test_user_pref_creation(self):
        self.assertNotEqual(self.userprefs, None)


class TestUserDogModel(TestCase):
    def setUp(self):
        self.ryan = User.objects.create(
            username='ryan',
            password='ryan')
        self.dog = Dog.objects.create(
            name='max',
            image_filename='maxpic',
            breed='dachsund',
            age=8
        )
        self.userdog = UserDog.objects.create(
            user=self.ryan,
            dog=self.dog,
            status='l'
        )

    def test_user_dog_creation(self):
        userdog = UserDog.objects.get(
            user=self.ryan,
            dog=self.dog
        )
        self.assertNotEqual(userdog, None)


class TestAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        Dog.objects.create(
            name='max',
            image_filename='maxpic',
            breed='dachsund',
            age=40,
            size='s',
            gender='m'
        ),
        Dog.objects.create(
            name='floyd',
            image_filename='floydpic',
            breed='German shepherd',
            age=5,
            size='m',
            gender='f'
        ),
        Dog.objects.create(
            name='george',
            image_filename='georgepic',
            breed='terrier',
            age=73,
            size='l',
            gender='m'
        ),
        Dog.objects.create(
            name='teddy',
            image_filename='teddypic',
            breed='basset hound',
            age=7,
            size='xl',
            gender='f'
        )
        trixie = Dog.objects.create(
            name='trixie',
            image_filename='trixiepic',
            breed='basset hound',
            age=19,
            size='m',
            gender='f'
        )
        neo = Dog.objects.create(
            name='neo',
            image_filename='neopic',
            breed='mutt',
            age=17,
            size='l',
            gender='m'
        )
        user = User.objects.create(
            username='willie',
            password='willie'
        )

        # Set user's UserDog status for last two dogs to 'liked' and 'disliked'
        trixie_userdog = UserDog.objects.get(user=user, dog=trixie)
        neo_userdog = UserDog.objects.get(user=user, dog=neo)
        trixie_userdog.status = 'l'
        neo_userdog.status = 'd'
        trixie_userdog.save()
        neo_userdog.save()

    def test_register_user(self):
        response = self.client.post(
            reverse('register-user'),
            {'username': 'leah', 'password': 'leah'}
        )
        user = User.objects.get(username='leah')
        user_pref = UserPref.objects.get(user=user)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(user_pref, None)

    def test_get_preferences_no_auth(self):
        url = reverse('user-prefs')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 401)

    def test_update_preferences_with_token(self):
        url = reverse('user-prefs')
        user = User.objects.get(username='willie')
        token, created = Token.objects.get_or_create(user=user)
        data = {'user': user.id, 'age': 'b,y,a', 'gender': 'f', 'size': 'm,l'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.put(url, data, format='json')
        userprefs = UserPref.objects.get(user=user.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(userprefs.age, 'b,y,a')
        self.assertEqual(userprefs.gender, 'f')
        self.assertEqual(userprefs.size, 'm,l')

    def test_get_first_undecided_dog(self):
        kwargs = {'pk': '-1', 'decision': 'undecided'}
        url = reverse('get-next-dog', kwargs=kwargs)
        user = User.objects.get(username='willie')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_next_undecided_dog(self):
        kwargs = {'pk': '1', 'decision': 'undecided'}
        url = reverse('get-next-dog', kwargs=kwargs)
        user = User.objects.get(username='willie')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_first_liked_dog(self):
        kwargs = {'pk': '-1', 'decision': 'liked'}
        url = reverse('get-next-dog', kwargs=kwargs)
        user = User.objects.get(username='willie')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_first_disliked_dog(self):
        kwargs = {'pk': '-1', 'decision': 'disliked'}
        url = reverse('get-next-dog', kwargs=kwargs)
        user = User.objects.get(username='willie')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_like_dog(self):
        kwargs = {'pk': '1', 'decision': 'liked'}
        url = reverse('decide', kwargs=kwargs)
        user = User.objects.get(username='willie')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, 201)

    def test_dislike_dog(self):
        kwargs = {'pk': '1', 'decision': 'disliked'}
        url = reverse('decide', kwargs=kwargs)
        user = User.objects.get(username='willie')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, 201)

    def test_undecide_dog(self):
        kwargs = {'pk': '1', 'decision': 'undecided'}
        url = reverse('decide', kwargs=kwargs)
        user = User.objects.get(username='willie')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, 201)
