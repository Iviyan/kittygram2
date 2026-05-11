from rest_framework import serializers

from .models import Trip, Stop


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = (
            'id', 'location_name', 'arrival_date',
            'departure_date', 'notes', 'order',
        )

    def validate(self, data):
        if data.get('departure_date') and data.get('arrival_date'):
            if data['departure_date'] < data['arrival_date']:
                raise serializers.ValidationError(
                    'Дата отъезда не может быть раньше даты прибытия.'
                )
        view = self.context.get('view')
        order = data.get('order')
        if view and order is not None:
            trip_pk = view.kwargs.get('trip_pk')
            qs = Stop.objects.filter(trip_id=trip_pk, order=order)
            if self.instance is not None:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    'order': 'В этой поездке уже есть остановка с таким порядковым номером.'
                })
        return data


class TripSerializer(serializers.ModelSerializer):
    stops = StopSerializer(many=True, read_only=True)
    stops_count = serializers.IntegerField(
        source='stops.count', read_only=True
    )
    cat_name = serializers.StringRelatedField(source='cat', read_only=True)

    class Meta:
        model = Trip
        fields = (
            'id', 'cat', 'cat_name', 'title', 'status', 'start_date',
            'end_date', 'notes', 'stops', 'stops_count', 'created_at',
        )
        read_only_fields = ('status', 'created_at')

    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError(
                    'Дата окончания не может быть раньше даты начала.'
                )
        request = self.context.get('request')
        cat = data.get('cat')
        if cat and request and cat.owner != request.user:
            raise serializers.ValidationError(
                'Вы можете создавать поездки только для своих котов.'
            )
        return data


class TripListSerializer(serializers.ModelSerializer):
    cat_name = serializers.StringRelatedField(source='cat', read_only=True)
    stops_count = serializers.IntegerField(
        source='stops.count', read_only=True
    )

    class Meta:
        model = Trip
        fields = (
            'id', 'cat', 'cat_name', 'title', 'status',
            'start_date', 'end_date', 'stops_count', 'created_at',
        )
