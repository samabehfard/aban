from django.core.management.base import BaseCommand, CommandError

from purchase.models import Wallet, Transaction
from users.models import User


class Command(BaseCommand):
    help = 'Create a test user with a specified USDT balance.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the new user')
        parser.add_argument('usdt_balance', type=float, help='The initial USDT balance for the user')

    def handle(self, *args, **options):
        username = options['username']
        usdt_balance = options['usdt_balance']

        # Validate the input balance
        if usdt_balance < 0:
            raise CommandError("The USDT balance must be a positive value.")

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            raise CommandError(f"User '{username}' already exists.")

        # Create the user
        user = User.objects.create_user(username=username)
        self.stdout.write(self.style.SUCCESS(f"User '{username}' created successfully."))

        # Create the USDT wallet
        w = Wallet.get_for(user=user, currency_name="USDT")
        Transaction.objects.create(source=w, amount=usdt_balance)
        self.stdout.write(self.style.SUCCESS(f"USDT wallet with balance {usdt_balance} created for user '{username}'."))
