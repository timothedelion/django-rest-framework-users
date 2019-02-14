from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse
from rest_framework import status

from main.models import Profile
from main.serializers import ListUserSerializer, DetailUserSerializer

client = Client()


class URLTests(TestCase):

    def setUp(self):
        # Jake, 28 ans
        self.jake = User.objects.create(username='Jake', password='azerty')
        Profile.objects.create(user=self.jake, birthday=datetime.strptime('13/11/1990', '%d/%m/%Y').date())
        # Amanda, 3 ans
        self.amanda = User.objects.create(username='Amanda', password='azerty')
        Profile.objects.create(user=self.amanda, birthday=datetime.strptime('11/02/2016', '%d/%m/%Y').date())

    def test_URL_list(self):
        """
        Test du EndPoint de list
        :return:
        """
        response = client.get(reverse('main:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_URL_detail(self):
        """
        Test du EndPoint de Detail
        :return:
        """
        response = client.get(reverse('main:user-detail', kwargs={'pk': self.jake.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllUserTest(TestCase):
    """Test des données recues de l'API sur l'URL user-list"""

    def setUp(self):
        # Jake, 28 ans
        self.jake = User.objects.create(username='Jake', password='azerty')
        Profile.objects.create(user=self.jake, birthday=datetime.strptime('13/11/1990', '%d/%m/%Y').date())
        # Amanda, 3 ans
        self.amanda = User.objects.create(username='Amanda', password='azerty')
        Profile.objects.create(user=self.amanda, birthday=datetime.strptime('11/02/2016', '%d/%m/%Y').date())

    def test_get_all_users(self):
        """
        Test des données recues de l'API sur l'URL user-list
        :return:
        """
        # Réponse de l'API :
        response = client.get(reverse('main:user-list'))
        # Données depuis la DB :
        users = User.objects.all()
        serializer = ListUserSerializer(users, many=True)
        # Verification :
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleUserTest(TestCase):
    """Test des données recues de l'API sur l'URL user-detail"""

    def setUp(self):
        # Jake, 28 ans
        self.jake = User.objects.create(username='Jake', password='azerty')
        Profile.objects.create(user=self.jake, birthday=datetime.strptime('13/11/1990', '%d/%m/%Y').date())
        # Amanda, 3 ans
        self.amanda = User.objects.create(username='Amanda', password='azerty')
        Profile.objects.create(user=self.amanda, birthday=datetime.strptime('11/02/2016', '%d/%m/%Y').date())

    def test_get_valid_single_user(self):
        # Reponse de l'API :
        response = client.get(reverse('main:user-detail', kwargs={'pk': self.jake.pk}))
        # Données de la DB :
        serializer = DetailUserSerializer(self.jake)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = client.get(reverse('main:user-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetFilteredUserTest(TestCase):
    """Test des données recues de l'API sur l'URL user-list, avec des query parameter de filtrage"""

    def setUp(self):
        # Jake, 28 ans
        self.jake = User.objects.create(username='Jake', password='azerty')
        Profile.objects.create(user=self.jake, birthday=datetime.strptime('13/11/1990', '%d/%m/%Y').date())
        # Amanda, 3 ans
        self.amanda = User.objects.create(username='Amanda', password='azerty')
        Profile.objects.create(user=self.amanda, birthday=datetime.strptime('11/02/2016', '%d/%m/%Y').date())

    def test_annee_naissance_valid(self):
        year = 2016
        # Reponse de l'API :
        url = reverse('main:user-list') + '?year={}'.format(str(year))
        response = client.get(url)
        # Données de la DB :
        queryset = User.objects.filter(profile__birthday__year=year)
        serializer = ListUserSerializer(queryset, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_annee_naissance_invalid(self):
        year = 2017
        # Reponse de l'API :
        url = reverse('main:user-list') + '?year={}'.format(str(year))
        response = client.get(url)
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_age_min(self):
        age_min = 4
        # Reponse de l'API :
        url = reverse('main:user-list') + '?age_min={}'.format(str(age_min))
        response = client.get(url)
        # Données de la DB :
        queryset = User.objects.filter(username='Jake')
        serializer = ListUserSerializer(queryset, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_age_max(self):
        age_max = 27
        # Reponse de l'API :
        url = reverse('main:user-list') + '?age_max={}'.format(str(age_max))
        response = client.get(url)
        # Données de la DB :
        queryset = User.objects.filter(username='Amanda')
        serializer = ListUserSerializer(queryset, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_age_exact_valid(self):
        age_exact = 3
        # Reponse de l'API :
        url = reverse('main:user-list') + '?age_exact={}'.format(str(age_exact))
        response = client.get(url)
        # Données de la DB :
        queryset = User.objects.filter(username='Amanda')
        serializer = ListUserSerializer(queryset, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_age_exact_invalid(self):
        age_exact = 4
        # Reponse de l'API :
        url = reverse('main:user-list') + '?age_exact={}'.format(str(age_exact))
        response = client.get(url)
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

