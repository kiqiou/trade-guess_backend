from django.contrib import admin

from core.models.user import (
    Role,
    User,
    DailyStatistics,
    UserStatistics
)

from core.models.game import (
    Asset,
    ChartSnapshot,
    Attempt
)

admin.site.register(Role)
admin.site.register(User)
admin.site.register(DailyStatistics)
admin.site.register(UserStatistics)

admin.site.register(Asset)
admin.site.register(ChartSnapshot)
admin.site.register(Attempt)
