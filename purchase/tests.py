from django.test import TestCase

from purchase.errors import InsufficientBalanceError
from purchase.logic.purchase_logic import PurchaseLogic
from purchase.models import Transaction, Wallet
from users.models import User


class TestPurchase(TestCase):
    def test_purchase_greater_10_dollar(self):
        p = PurchaseLogic()
        u = User.objects.create(username="ihih")
        Transaction.objects.create(amount=70, source=Wallet.get_for(user=u, currency_name="USDT"))
        self.assertEqual(Wallet.get_for(user=u, currency_name="USDT").amount, 70)
        p.purchase("ihih", "BTC", 10)
        assert Transaction.objects.all().count() == 5
        self.assertEqual(Wallet.get_for(user=u, currency_name="BTC").amount, 10)
        self.assertEqual(Wallet.get_for(user=u, currency_name="USDT").amount, 30)

    def test_purchase_under_10_dollar(self):
        p = PurchaseLogic()
        u = User.objects.create(username="ihih")
        Transaction.objects.create(amount=70, source=Wallet.get_for(user=u, currency_name="USDT"))
        p.purchase("ihih", "BTC", 1)
        self.assertEqual(Wallet.get_for(user=u, currency_name="BTC").amount, 0)
        self.assertEqual(Wallet.get_for(user=u, currency_name="USDT").amount, 66)

        p.purchase("ihih", "BTC", 1)
        self.assertEqual(Wallet.get_for(user=u, currency_name="BTC").amount, 0)
        self.assertEqual(Wallet.get_for(user=u, currency_name="USDT").amount, 62)

        p.purchase("ihih", "BTC", 1)
        self.assertEqual(Wallet.get_for(user=u, currency_name="BTC").amount, 3)
        self.assertEqual(Wallet.get_for(user=u, currency_name="USDT").amount, 58)

    def test_purchase_under_10_dollar_with_insufficient(self):

        p = PurchaseLogic()
        u = User.objects.create(username="ihih")
        try:
            p.purchase("ihih", "BTC", 10)
        except InsufficientBalanceError as e:
            ...
        except Exception:
            assert False
