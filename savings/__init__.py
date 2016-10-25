from abc import ABCMeta, abstractmethod
from typing import Callable, Optional


class PresentRequiredEarningsObserver(metaclass=ABCMeta):
    @abstractmethod
    def did_present_required_earnings(self, required_earnings: float):
        pass


class SavingsObserver(metaclass=ABCMeta):
    @abstractmethod
    def register_savings_functions(self, present_required_earnings: Callable[[int,
                                                                              float,
                                                                              PresentRequiredEarningsObserver],
                                                                             None]):
        pass


class Savings(object):
    def __init__(self, savings_observer: Optional[SavingsObserver]):
        super().__init__()
        self._savings_observer = savings_observer

    @staticmethod
    def present_required_earnings(tax_rate: int,
                                  desired_savings: float,
                                  observer: PresentRequiredEarningsObserver) -> None:
        required_earnings = 1 / ((1 - (tax_rate * .01)) / desired_savings)
        observer.did_present_required_earnings(required_earnings)

    def start(self):
        if self._savings_observer:
            self._savings_observer.register_savings_functions(present_required_earnings=self.present_required_earnings)
