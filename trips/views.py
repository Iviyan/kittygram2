from django.shortcuts import get_object_or_404
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Trip, Stop
from kittygram2.permissions import IsOwnerOrReadOnly
from .serializers import StopSerializer, TripListSerializer, TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'cat__name']
    ordering_fields = ['start_date', 'created_at']

    def get_queryset(self):
        qs = Trip.objects.filter(owner=self.request.user)
        cat_id = self.request.query_params.get('cat')
        if cat_id:
            qs = qs.filter(cat_id=cat_id)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs.select_related('cat').prefetch_related('stops')

    def get_serializer_class(self):
        if self.action == 'list':
            return TripListSerializer
        return TripSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """POST /trips/{id}/complete/ — завершить поездку."""
        trip = self.get_object()
        if trip.status != 'active':
            return Response(
                {'detail': 'Завершить можно только активную поездку.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trip.status = 'completed'
        trip.save()
        return Response(TripSerializer(trip, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """POST /trips/{id}/activate/ — начать поездку."""
        trip = self.get_object()
        if trip.status != 'planned':
            return Response(
                {'detail': 'Только запланированную поездку можно активировать.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trip.status = 'active'
        trip.save()
        return Response(TripSerializer(trip, context={'request': request}).data)


class StopViewSet(viewsets.ModelViewSet):
    serializer_class = StopSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Stop.objects.filter(
            trip_id=self.kwargs['trip_pk'],
            trip__owner=self.request.user,
        )

    def perform_create(self, serializer):
        trip = get_object_or_404(
            Trip, pk=self.kwargs['trip_pk'], owner=self.request.user
        )
        if trip.status == 'completed':
            raise serializers.ValidationError(
                'Нельзя добавить остановку в завершённую поездку.'
            )
        serializer.save(trip=trip)
