from django.core.management.base import NoArgsCommand
from forum.models import User
import sys
import messages_extends

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        msg = None
        if msg == None:
            print 'to run this command, please first edit the file %s' % __file__
            sys.exit(1)
        for u in User.objects.all():
            u.message_set.create(message = msg % u.username, level=messages_extends.SUCCESS_PERSISTENT)
