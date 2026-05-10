from django.contrib import admin

from .models import Achievement, AchievementCat, Cat


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'birth_year', 'owner')
    list_filter = ('color',)
    search_fields = ('name', 'owner__username')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(AchievementCat)
class AchievementCatAdmin(admin.ModelAdmin):
    list_display = ('achievement', 'cat')
    search_fields = ('achievement__name', 'cat__name')
