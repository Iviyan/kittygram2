from django.contrib import admin

from .models import Stop, Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'cat', 'owner', 'status', 'start_date', 'end_date')
    list_filter = ('status',)
    search_fields = ('title', 'cat__name', 'owner__username')


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'trip', 'arrival_date', 'departure_date', 'order')
    search_fields = ('location_name', 'trip__title')
