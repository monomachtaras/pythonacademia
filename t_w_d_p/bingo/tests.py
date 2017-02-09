from django.test import TestCase

from .models import Number


class NumberTests(TestCase):

    def test_equality(self):
        """ test if method equals works fine
        """
        # number = Number.objects.get(number=56412)
        number1 = Number(number=56412)
        number2 = Number(number=556415)

        self.assertIs(number1.__eq__(number1), True)
        self.assertIs(number1.__eq__(number2), False)
