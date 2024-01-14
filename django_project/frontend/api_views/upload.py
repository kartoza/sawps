# -*- coding: utf-8 -*-

"""API Views for uploading file.
"""
import os
from datetime import datetime
from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from fiona.crs import from_epsg
from frontend.models.base_task import DONE
from frontend.models.boundary_search import (
    BoundaryFile,
    GEOJSON,
    GEOPACKAGE,
    SHAPEFILE,
    KML,
    BoundarySearchRequest
)
from frontend.utils.upload_file import (
    validate_shapefile_zip,
    get_uploaded_file_crs
)
from frontend.serializers.boundary_file import (
    BoundaryFileSerializer,
    BoundarySearchRequestGeoJsonSerializer
)
from frontend.tasks.parcel import boundary_files_search


class BoundaryFileUpload(APIView):
    """Upload Boundary File."""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def check_file_type(self, filename: str) -> str:
        if (filename.lower().endswith('.geojson') or
                filename.lower().endswith('.json')):
            return GEOJSON
        elif filename.lower().endswith('.zip'):
            return SHAPEFILE
        elif filename.lower().endswith('.gpkg'):
            return GEOPACKAGE
        elif filename.lower().endswith('.kml'):
            return KML
        return ''

    def validate_shapefile_zip(self, file_obj: any) -> str:
        _, error = validate_shapefile_zip(file_obj)
        if error:
            return ('Missing required file(s) inside zip file: \n- ' +
                    '\n- '.join(error) +
                    '\n Please make sure it is a valid zip file and '
                    'the shp file is at the root directory of the zip package'
                    )
        return ''

    def remove_temp_file(self, file_obj: any) -> None:
        if isinstance(file_obj, TemporaryUploadedFile):
            if os.path.exists(file_obj.temporary_file_path()):
                os.remove(file_obj.temporary_file_path())

    def check_crs_type(self, file_obj: any, type: any):
        epsg_mapping = from_epsg(4326)
        crs = get_uploaded_file_crs(file_obj, type)
        return crs.upper() == epsg_mapping['init'].upper(), crs

    def post(self, request, format=None):
        file_obj = request.FILES['file']
        session = request.data.get('session', '')
        file_type = self.check_file_type(file_obj.name)
        if file_type == '':
            self.remove_temp_file(file_obj)
            return Response(
                status=400,
                data={
                    'detail': 'Unrecognized file type!'
                }
            )
        if file_type == SHAPEFILE:
            validate_shp_file = self.validate_shapefile_zip(file_obj)
            if validate_shp_file != '':
                self.remove_temp_file(file_obj)
                return Response(
                    status=400,
                    data={
                        'detail': validate_shp_file
                    }
                )
        is_valid_crs, crs = self.check_crs_type(file_obj, file_type)
        if not is_valid_crs:
            self.remove_temp_file(file_obj)
            return Response(
                status=400,
                data={
                    'detail': f'Incorrect CRS type: {crs}!'
                }
            )
        BoundaryFile.objects.create(
            name=file_obj.name,
            session=session,
            uploader=self.request.user,
            file_type=file_type,
            meta_id=request.data.get('meta_id', ''),
            upload_date=datetime.now(),
            file=file_obj
        )
        self.remove_temp_file(file_obj)
        return Response(status=204)


class BoundaryFileRemove(APIView):
    """Remove Boundary File."""
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        file_meta_id = request.data.get('meta_id')
        session = request.data.get('session')
        boundary_file = BoundaryFile.objects.filter(
            session=session,
            meta_id=file_meta_id
        )
        if not boundary_file.exists():
            return Response(status=200)
        boundary_file.delete()
        return Response(status=200)


class BoundaryFileList(APIView):
    """Retrieve Uploaded Boundary Files."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        session = kwargs.get('session')
        boundary_files = BoundaryFile.objects.filter(
            session=session
        ).order_by('id')
        return Response(
            status=200,
            data=BoundaryFileSerializer(
                boundary_files, many=True
            ).data
        )


class BoundaryFileSearch(APIView):
    """Find parcel by boundary files."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        session = kwargs.get('session')
        search_type = self.request.GET.get('search_type', 'File')
        # create new boundary search request
        boundary_search = BoundarySearchRequest.objects.create(
            type=search_type,
            session=session,
            request_by=self.request.user
        )
        task = boundary_files_search.delay(boundary_search.id)
        boundary_search.task_id = task.id
        boundary_search.save(update_fields=['task_id'])
        return Response(status=204)


class BoundaryFileSearchStatus(APIView):
    """Check status search parcel by boundary files."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        session = kwargs.get('session')
        search_request = BoundarySearchRequest.objects.filter(
            session=session
        ).order_by('-id').first()
        if not search_request:
            return Response(status=404)
        return Response(
            status=200,
            data={
                'status': search_request.status,
                'parcels': search_request.parcels,
                'used_parcels': search_request.used_parcels,
                'bbox': (
                    list(search_request.geometry.extent) if
                    search_request.geometry else []
                )
            }
        )


class BoundaryFileGeoJson(APIView):
    """Get geojson from search request."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        session = kwargs.get('session')
        search_request = BoundarySearchRequest.objects.filter(
            session=session
        ).order_by('-id').first()
        if not search_request:
            return Response(status=404)
        if search_request.status != DONE:
            return Response(status=404)
        if not search_request.geometry:
            return Response(status=404)
        return Response(
            status=200,
            data=BoundarySearchRequestGeoJsonSerializer(search_request).data
        )
