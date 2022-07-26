from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        res2 = self.client.get(DRIVER_URL)
        res3 = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)
        self.assertNotEqual(res2.status_code, 200)
        self.assertNotEqual(res3.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers_and_cars(self):
        manufacturer1 = Manufacturer.objects.create(name="BMW")
        manufacturer2 = Manufacturer.objects.create(name="Mersedes")

        Car.objects.create(model="X5", manufacturer=manufacturer1)
        Car.objects.create(model="X5", manufacturer=manufacturer2)

        response = self.client.get(MANUFACTURERS_URL)
        response2 = self.client.get(CAR_URL)

        manufacturers = Manufacturer.objects.all()
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            list(response2.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response2, "taxi/car_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test First",
            "last_name": "Last name",
            "license_number": "ABC12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(new_driver.license_number, form_data["license_number"])

