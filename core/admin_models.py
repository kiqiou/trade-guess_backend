from django.contrib import admin
from django.contrib.auth.models import User
from .models.game import UserStat, Attempt, Asset, ChartFragment

@admin.register(UserStat)
class UserStatAdmin(admin.ModelAdmin):
    list_display = ("user", "total_attempts", "total_successes", "accuracy", "streak")
    search_fields = ("user__username",)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "direction", "success", "created_at")
    list_filter = ("success", "direction")
    search_fields = ("user__username",)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "symbol")

@admin.register(ChartFragment)
class ChartFragmentAdmin(admin.ModelAdmin):
    list_display = ("id", "asset", "created_at")


# --- BAN SYSTEM ---

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    actions = ["ban_users", "unban_users"]

    @admin.action(description="Забанить пользователей")
    def ban_users(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Разбанить пользователей")
    def unban_users(self, request, queryset):
        queryset.update(is_active=True)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
