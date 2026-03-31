from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from pets.models import Pet, Vaccination
from .serializers import PetSerializer, VaccinationSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def vaccinations(self, request, pk=None):
        pet = self.get_object()
        vaccinations = pet.vaccinations.all()
        serializer = VaccinationSerializer(vaccinations, many=True)
        return Response(serializer.data)