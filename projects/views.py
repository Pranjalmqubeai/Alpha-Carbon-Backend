# projects/views.py
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Project
from .serializers import ProjectSer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related(
        "images", "impacts", "vintages", "docs", "transactions"
    )
    serializer_class = ProjectSer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country", "kind", "info_registry"]
    search_fields = ["title", "country", "info_company", "id"]
    ordering_fields = ["price", "sdg_score", "created_at"]