from django.core.management.base import BaseCommand, CommandError

from vidtrest.apps.vid.signals import do_video_thumbs
from vidtrest.apps.vid.models import Vid

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('video_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for video_id in options['video_id']:
            try:
                video = Vid.objects.get(pk=video_id)
            except Vid.DoesNotExist:
                raise CommandError('Video "%s" does not exist' % video_id)

            do_video_thumbs(instance=video, video=video.video)

            self.stdout.write(self.style.SUCCESS('Successfully procesed video "%s"' % video_id))