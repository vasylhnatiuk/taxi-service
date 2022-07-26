from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_create_driver_with_license(self):
        form_data = {
            "username": "new_user",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test First",
            "last_name": "Last name",
            "license_number": "ABC12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_create_with_wrong_license(self):
        wrong_license = {
            "username": "new_user",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test First",
            "last_name": "Last name",
            "license_number": "ABC345"
        }

        form = DriverCreationForm(data=wrong_license)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, wrong_license)



