from django.core.management.base import BaseCommand
from agri.models import CropAdvice

class Command(BaseCommand):
    help = 'Load sample crop advice data'

    def handle(self, *args, **kwargs):
        CropAdvice.objects.all().delete()
        CropAdvice.objects.create(
            crop='Wheat', region='Kolhapur, Maharashtra',
            what_to_do='Grow wheat (suitable for Kolhapur, Maharashtra)',
            how_to_do='Prepare well-drained loamy soil, use certified seeds, irrigate at critical stages, manage weeds and pests',
            when_to_do='Sow in late November to early December, harvest in March-April'
        )
        CropAdvice.objects.create(
            crop='Rice', region='Maharashtra',
            what_to_do='Cultivate rice in Kharif season',
            how_to_do='Flood fields, transplant seedlings, manage pests',
            when_to_do='Sow in June-July, harvest in October-November'
        )
        CropAdvice.objects.create(
            crop='Sugarcane', region='Maharashtra',
            what_to_do='Plant sugarcane in well-prepared fields',
            how_to_do='Use healthy setts, maintain soil moisture, control pests',
            when_to_do='Plant in December-February, harvest after 12-18 months'
        )
        self.stdout.write(self.style.SUCCESS('Sample crop advice data loaded.'))
