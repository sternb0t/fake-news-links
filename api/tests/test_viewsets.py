from datetime import datetime, timedelta
from decimal import Decimal

from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from api.models import FakeNewsLink, FakeNewsLinkAttribute

class ApiViewsetsTests(APITestCase):

    def setUp(self):
        self.user, _= User.objects.get_or_create(username="testuser")
        content_type = ContentType.objects.get_for_model(FakeNewsLink)
        perms = Permission.objects.filter(content_type=content_type)
        self.user.user_permissions.set([p for p in perms])
        self.client.force_authenticate(self.user)

    def test_fakenews_links_crud(self):
        """
        Ensure we can create and read a FakeNewsLink object.
        """
        # create
        url = reverse('api:fakenews-links-list')
        data = {'url': 'http://something.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FakeNewsLink.objects.count(), 1)
        self.assertEqual(FakeNewsLink.objects.get().url, 'http://something.com')

        pk = response.json()["id"]

        # read and check data
        self.__read_link_assert(pk)

    def test_fakenews_links_crud_with_location(self):
        """
        Ensure we can create and read a FakeNewsLink object including location data.
        """
        # create
        url = reverse('api:fakenews-links-list')
        data = {
            "url": 'http://something.com',
            "longitude": 1.234567,
            "latitude": 9.987654,
            "geo_accuracy": 42
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FakeNewsLink.objects.count(), 1)
        obj = FakeNewsLink.objects.get()
        self.assertEqual(obj.url, 'http://something.com')
        self.assertEqual(obj.longitude, Decimal("1.234567"))
        self.assertEqual(obj.latitude, Decimal("9.987654"))
        self.assertEqual(obj.geo_accuracy, 42)

        pk = response.json()["id"]

        # read and check data
        data = self.__read_link_assert(pk)

        # check location fields
        self.assertEqual(data["longitude"], 1.234567)
        self.assertEqual(data["latitude"], 9.987654)
        self.assertEqual(data["geo_accuracy"], 42)


    def test_fakenews_links_crud_with_location_attributes(self):
        """
        Ensure we can create and read a FakeNewsLink object including location and attributes.
        """
        # create
        url = reverse('api:fakenews-links-list')
        data = {
            "url": 'http://something.com',
            "longitude": 1.234567,
            "latitude": 9.987654,
            "geo_accuracy": 42,
            "attributes": [
                {"id": 1}, {"id": 2}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FakeNewsLink.objects.count(), 1)
        obj = FakeNewsLink.objects.get()
        self.assertEqual(obj.url, 'http://something.com')
        self.assertEqual(obj.longitude, Decimal("1.234567"))
        self.assertEqual(obj.latitude, Decimal("9.987654"))
        self.assertEqual(obj.geo_accuracy, 42)

        # make sure attributes were linked correctly
        first_two_attributes = FakeNewsLinkAttribute.objects.filter(pk__in=(1, 2)).order_by("pk")
        self.assertEqual(list(obj.attributes.all().order_by("pk")), list(first_two_attributes))

        pk = response.json()["id"]

        # read and check data
        data = self.__read_link_assert(pk)

        # check location fields
        self.assertEqual(data["longitude"], 1.234567)
        self.assertEqual(data["latitude"], 9.987654)
        self.assertEqual(data["geo_accuracy"], 42)

        # check attributes
        self.assertEqual(data["attributes"], list(first_two_attributes.values("id", "name")))

    def __read_link_assert(self, pk):
        """
        get a fake news link from the API for a pk and assert basic data
        """
        url = reverse('api:fakenews-links-detail', kwargs={"pk": pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], pk)
        self.assertEqual(data["url"], "http://something.com")
        self.assertIn("created_date", data)
        self.assertIn("updated_date", data)

        for field in ["created_date", "updated_date"]:
            # make sure field is a proper datetime through instantiation
            dt = datetime.strptime(data[field], "%Y-%m-%dT%H:%M:%S.%fZ")
            # make sure date object is really UTC
            self.assertLess(datetime.utcnow() - dt, timedelta(seconds=1))

        return data

    def test_fakenews_attributes_crud(self):
        """
        Ensure we can read fake news links attributes
        """
        # create
        url = reverse('api:fakenews-attributes-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], len(data["results"]))


