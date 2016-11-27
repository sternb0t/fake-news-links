from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from api import models as api_models


class ApiModelsTests(TestCase):

    def test_user_crud(self):
        obj = api_models.FakeNewsLink()
        self.assertTrue(hasattr(obj, "url"))
        self.assertTrue(hasattr(obj, "created_date"))
        self.assertTrue(hasattr(obj, "updated_date"))

        obj.url = "http://something.com"
        obj.save()
        pk = obj.pk

        obj_again = api_models.FakeNewsLink.objects.get(pk=pk)
        self.assertEqual(obj_again.url, "http://something.com")

        obj.url = "http://somethingelse.com"
        obj.save()

        user_again = api_models.FakeNewsLink.objects.get(pk=pk)
        self.assertEqual(user_again.url, "http://somethingelse.com")

        obj.delete()

        with self.assertRaises(ObjectDoesNotExist):
            api_models.FakeNewsLink.objects.get(pk=pk)
