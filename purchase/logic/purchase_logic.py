from django.db import transaction

from purchase.adapter.exchange import ExchangeAdapter
from purchase.errors import CryptoNotFoundError, UserNotFoundError, InsufficientBalanceError
from purchase.models import Transaction, Wallet, WaitingListEntry
from users.models import User

# Constants
BROKERS_MIN_TOTAL = 10
CRYPTO_CURRENCIES = {"BTC": 4,"ETH":3}


class PurchaseLogic:
    def __init__(self):
        self.exchange_adapter = ExchangeAdapter()
        self.aban_user, _ = User.objects.get_or_create(username="AbanTether")

    def purchase(self, username, currency_name, count):
        # Check if the currency is supported
        if currency_name not in CRYPTO_CURRENCIES:
            raise CryptoNotFoundError()

        # Calculate total cost
        total = CRYPTO_CURRENCIES[currency_name] * count

        # Fetch user and wallets
        user = self.get_user(username)
        source_usdt_wallet = Wallet.get_for(user, "USDT")
        destination_usdt_wallet = Wallet.get_for(self.aban_user, "USDT")

        # Perform the transaction if the user has sufficient balance
        if total > source_usdt_wallet.amount:
            raise InsufficientBalanceError()

        self.create_transaction(-total, source_usdt_wallet)
        self.create_transaction(total, destination_usdt_wallet)

        if total >= BROKERS_MIN_TOTAL:
            self.buy(data=[{"user": user, "count": count}], currency_name=currency_name)
        else:
            self.handle_waiting_list(user, count, currency_name, total)

    def buy(self, data, currency_name="BTC"):
        total_count = sum(item["count"] for item in data)

        with transaction.atomic():
            if self.exchange_adapter.buy_from_exchange(name=currency_name, count=total_count):
                for item in data:
                    self.process_individual_purchase(item['user'], item['count'], currency_name)

                # Clear waiting list entries
                WaitingListEntry.objects.filter(currency_name=currency_name).delete()

    def process_individual_purchase(self, user, count, currency_name):
        destination_crypto_wallet = Wallet.get_for(user=self.aban_user, currency_name=currency_name)
        source_crypto_wallet = Wallet.get_for(user=user, currency_name=currency_name)

        self.create_transaction(-count, destination_crypto_wallet)
        self.create_transaction(count, source_crypto_wallet)

    def handle_waiting_list(self, user, count, currency_name, total):
        # Add user to waiting list
        entry, created = WaitingListEntry.objects.get_or_create(
            user=user,
            currency_name=currency_name,
            defaults={'count': count}
        )

        if not created:
            entry.count += count
            entry.save()

        waitings_total = sum(
            entry.count * CRYPTO_CURRENCIES[entry.currency_name] for entry in
            WaitingListEntry.objects.filter(currency_name=currency_name)
        )

        # If the total in the waiting list is sufficient, process the purchase
        if waitings_total >= BROKERS_MIN_TOTAL:
            waiting_entries = WaitingListEntry.objects.filter(currency_name=currency_name)
            data = [{'user': entry.user, 'count': entry.count} for entry in waiting_entries]
            self.buy(data=data, currency_name=currency_name)

    def get_user(self, username):
        user = User.objects.filter(username=username).first()
        if not user:
            raise UserNotFoundError()
        return user

    def create_transaction(self, amount, wallet):
        Transaction.objects.create(amount=amount, source=wallet)
