import json
from django.core.management.base import BaseCommand, CommandError
from property.spatial_data import *


class Command(BaseCommand):
    help = "Fetch spatial data for properties"

    def add_arguments(self, parser):
        parser.add_argument("property_ids", nargs="+", type=int)
        parser.add_argument("context_layer_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for property_id in options["property_ids"]:
            try:
                property_obj = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                raise CommandError('Property "%s" does not exist' % property_id)

            for context_layer_id in options['context_layer_ids']:
                try:
                    context_layer = ContextLayer.objects.get(id=context_layer_id)
                except Property.DoesNotExist:
                    raise CommandError('Context layer "%s" does not exist' % context_layer_id)

                spatial_data = extract_spatial_data_from_property_and_layer(
                    property_obj,
                    context_layer
                )
                self.stdout.write(
                    self.style.SUCCESS(json.dumps(spatial_data, indent=4))
                )

            self.stdout.write(
                self.style.SUCCESS('Successfully fetched spatial data "%s"' % property_obj.name)
            )
