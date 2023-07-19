import factory
from swaps.models import UploadSession
from stakeholder.factories import userFactory


class UploadSessionF(factory.django.DjangoModelFactory):
    """
    Upload session factory
    """
    class Meta:
        model = UploadSession
    uploader = factory.SubFactory(userFactory)
