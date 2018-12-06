from django.core.management.base import BaseCommand
import UserFactory 
import ObjectFactory 
import AbstractFactory 

class Command(BaseCommand):
    help = 'Seeds the database.'

    def add_arguments(self, parser):
        parser.add_argument('--users',
            default=200,
            type=int,
            help='The number of fake users to create.')

    def handle(self, *args, **options):
        for _ in range(options['users']):
            UserFactory.create()