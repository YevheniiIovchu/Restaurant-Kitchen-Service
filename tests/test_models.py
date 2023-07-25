from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from restaurant.models import DishType, Dish


class ModelTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="test_name",
        )

        self.assertEqual(
            str(dish_type),
            dish_type.name
        )

    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="test_username",
            password="test_password123",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="test_dish_type_name")
        dish = Dish.objects.create(
            name="test_dish_name",
            description="test_description",
            price=11.11,
            dish_type=dish_type,
        )

        self.assertEqual(
            str(dish),
            dish.name
        )

    def test_create_cook(self):
        username = "test_username"
        password = "test_password123"
        first_name = "test_first"
        last_name = "test_last"
        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )
        self.assertTrue(cook.check_password(password))

    def test_get_absolute_url_for_cook(self):
        cook = get_user_model().objects.create_user(
            username="test_username",
            password="test_password123",
        )
        actual_url = cook.get_absolute_url()
        expected_url = reverse("restaurant:cook-detail", kwargs={"pk": cook.pk})

        self.assertEqual(actual_url, expected_url)
