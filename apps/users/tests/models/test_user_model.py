from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from users.factories import UserFactory


class UserModelTests(TestCase):

    def test_create_user(self):
        user = get_user_model().objects.create_user(email="test@exemple.fr", phone="+33123456789", password="test")
        self.assertEqual(user.email, "test@exemple.fr")
        self.assertEqual(user.phone, "+33123456789")
        self.assertTrue(user.check_password("test"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_confirm)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(phone="+33123456789", password="test")

    def test_create_user_email_is_None(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, phone="+33123456789", password="test")

    def test_create_user_without_phone(self):
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(email="test@exemple.fr", password="test")

    def test_create_user_phone_is_none(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(phone=None, email="test@exemple.fr", password="test")

    def test_create_user_without_password(self):
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(email="test@exemple.fr", phone="+33123456789")

    def test_create_user_with_group(self):
        new_group, _ = Group.objects.get_or_create(name='new_group')
        user = get_user_model().objects.create_user(
            email="test@exemple.fr", phone="+33123456789", password="test", group=new_group
        )
        self.assertEqual(user.groups.count(), 1)
        self.assertEqual(user.groups.first().id, new_group.id)
        self.assertEqual(user.groups.first(), new_group)

    def test_user_factory_empty(self):
        user = UserFactory()
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_confirm)
        self.assertTrue(user.check_password("default"))

    def test_user_factory(self):
        user = UserFactory(
            email="test@exemple.fr", phone="0123456789", first_name="Sarah", last_name="Croche",
            password="test"
        )
        self.assertEqual(user.first_name, "Sarah")
        self.assertEqual(user.last_name, "Croche")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_confirm)
        self.assertTrue(user.check_password("test"))

    def test_user_str(self):
        user = UserFactory(first_name="Alain", last_name="Proviste")
        self.assertEqual(user.__str__(), "Alain Proviste")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="test@exemple.fr", password="test"
        )
        self.assertEqual(user.first_name, "admin")
        self.assertEqual(user.last_name, "admin")
        self.assertEqual(user.email, "test@exemple.fr")
        self.assertEqual(user.phone, "0123456789")
        self.assertTrue(user.check_password("test"))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.is_confirm)

    def test_create_superuser_without_email(self):
        with self.assertRaises(TypeError):
            get_user_model().objects.create_superuser(password="test")

    def test_create_superuser_without_password(self):
        with self.assertRaises(TypeError):
            get_user_model().objects.create_superuser(email="test@exemple.fr")

    def test_create_superuser_is_staff_false(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                 is_staff=False, email="test@exemple.fr", password="test"
            )

    def test_create_superuser_is_superuser_false(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(is_superuser=False, email="test@exemple.fr", password="test")
