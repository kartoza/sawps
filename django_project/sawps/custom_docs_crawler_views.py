from docs_crawler.api.documentation import DocumentationDetail
from rest_framework.permissions import AllowAny


class CustomDocumentationDetail(DocumentationDetail):
    permission_classes = [AllowAny]
