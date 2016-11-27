from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from accounts import models as accounts_models


class AccountsModelsTests(TestCase):

    def test_user_crud(self):
        obj = accounts_models.User()
        self.assertTrue(hasattr(obj, "data"))
        self.assertTrue(hasattr(obj, "created_date"))
        self.assertTrue(hasattr(obj, "updated_date"))

        obj.data = {"kind": "human"}
        obj.save()
        pk = obj.pk

        obj_again = accounts_models.User.objects.get(pk=pk)
        self.assertEqual(obj_again.data, {"kind": "human"})

        obj.data["level"] = 42
        obj.save()

        obj_again = accounts_models.User.objects.get(pk=pk)
        self.assertEqual(obj_again.data, {"kind": "human", "level": 42})

        obj.delete()

        with self.assertRaises(ObjectDoesNotExist):
            accounts_models.User.objects.get(pk=pk)
