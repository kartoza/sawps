import json
import time
from celery.result import AsyncResult
from django.core.management.base import BaseCommand
from frontend.models.boundary_search import (
    BoundarySearchRequest, BoundaryFile
)
from frontend.serializers.boundary_file import (
    BoundaryFileSerializer,
    BoundarySearchRequestSerializer
)


class Command(BaseCommand):
    help = "Debug Boundary Search Request"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        time.sleep(60)
        last_request = BoundarySearchRequest.objects.last()
        if last_request:
            data = BoundarySearchRequestSerializer(last_request).data
            self.stdout.write(
                self.style.SUCCESS(json.dumps(data, indent=4))
            )
            self.stdout.write(
                self.style.SUCCESS('-------')
            )
            files = BoundaryFile.objects.filter(
                session=last_request.session
            )
            data = BoundaryFileSerializer(files, many=True).data
            self.stdout.write(
                self.style.SUCCESS(json.dumps(data, indent=4))
            )
            if last_request.task_id:
                res = AsyncResult(last_request.task_id)
                self.stdout.write(
                    self.style.SUCCESS(f'AsyncResult status: {res.state}')
                )
        else:
            self.stdout.write(
                self.style.ERROR('There is no boundary search request!')
            )
