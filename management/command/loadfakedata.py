
from django.core.management.base import BaseCommand
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth.models import User
from core.models import UserSettings
from ...models import Company
from ...factorboy import CompanyFactory
class Command(BaseCommand):
    args = 'username...'
    help = 'Populate company table with random dummy data.'

    def handle(self, *args, **options):
        if len(args) == 0:
            sys.stdout.write('You must specify a username.\n')
            sys.exit(1)

       try:
            user = User.objects.get(username=args[0])
       except ObjectDoesNotExist:
            user = User.objects.create(username=args[0])
            user.first_name = 'John'
            user.last_name = 'Smith'
            user.email = 'test@companytracker.net'
            user.set_password('demo')
            user.save()

            # Create an entry for the User Settings.
            UserSettings.objects.create(user=user).save()

        # Delete existing data.
        Company.objects.filter(user=user).delete()

        end_date = date.today()
        start_date = end_date - timedelta(days=90)
        for i in self.get_date_list(start_date, end_date):
            for _ in range(4):
               CompanyFactory(
                  user=user,
                   company=company,
                    year_established=year_established
               )

    @classmethod
    def get_date_list(cls, start, end):
        delta = end - start
       return [(start + timedelta(days=i)) for i in range(delta.days+1)]

