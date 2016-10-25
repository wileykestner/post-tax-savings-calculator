from typing import Callable
from unittest import TestCase

from savings import Savings, SavingsObserver, PresentRequiredEarningsObserver


class SimpleSavingsObserver(SavingsObserver):
    def __init__(self):
        super().__init__()
        self.callables = {}

    def register_savings_functions(self, present_required_earnings: Callable[[int,
                                                                              float,
                                                                              PresentRequiredEarningsObserver],
                                                                             None]):
        self.callables['my_special_function'] = present_required_earnings


class Captor(PresentRequiredEarningsObserver):
    def __init__(self):
        super().__init__()
        self.required_earnings = None

    def did_present_required_earnings(self, required_earnings: float):
        self.required_earnings = required_earnings


class TestSavingsWithOutObserver(TestCase):
    def setUp(self):
        super().setUp()
        self.subject = Savings(savings_observer=None)

    def test_present_required_earnings(self):
        observer = Captor()
        self.subject.present_required_earnings(tax_rate=35, desired_savings=1000.0, observer=observer)

        self.assertAlmostEqual(observer.required_earnings, 1538.4615384615388)


class TestSavingsWithObserver(TestCase):
    def setUp(self):
        super().setUp()
        self.observer = SimpleSavingsObserver()
        self.subject = Savings(savings_observer=self.observer)

    def test_present_required_earnings_with_start(self):
        self.subject.start()
        observer = Captor()
        self.observer.callables['my_special_function'](tax_rate=35, desired_savings=1000.0, observer=observer)

        self.assertAlmostEqual(observer.required_earnings, 1538.4615384615388)

    def test_present_required_earnings_without_start(self):
        self.assertIsNone(self.observer.callables.get('my_special_function', None))
