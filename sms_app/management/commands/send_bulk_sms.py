# sms_app/management/commands/send_bulk_sms.py
import time
from django.core.management.base import BaseCommand
from sms_app.services import send_sms_serial  # or send_sms_rpc

class Command(BaseCommand):
    help = 'Bulk send SMS to parents'

    def add_arguments(self, parser):
        parser.add_argument('--grade', type=str, help='Only send to parents of a specific grade')
        parser.add_argument('--message', type=str, required=True, help='SMS content')

    def handle(self, *args, **options):
        # Assume you have a Parent model with a phone_number field
        # from your_app.models import Parent
        # queryset = Parent.objects.all()
        # if options['grade']:
        #     queryset = queryset.filter(student__grade=options['grade'])

        # Replace with your actual model query
        parents = [
            {'name': 'Parent Zhang', 'phone': '8613800138000'},
            {'name': 'Parent Li', 'phone': '8613900139000'},
        ]

        message = options['message']
        success, fail = 0, 0

        for p in parents:
            phone = p['phone']
            ok = send_sms_serial(phone, message)  # or send_sms_rpc
            if ok:
                success += 1
                self.stdout.write(self.style.SUCCESS(f'✓ {phone} sent successfully'))
            else:
                fail += 1
                self.stderr.write(self.style.ERROR(f'✗ {phone} sending failed'))
            time.sleep(1.5)  # Avoid carrier rate limiting

        self.stdout.write(self.style.SUCCESS(f'Complete: success {success}, failure {fail}'))