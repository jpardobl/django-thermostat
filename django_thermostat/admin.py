from django.contrib import admin
from models import *


class RuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Rule, RuleAdmin)


class DayAdmin(admin.ModelAdmin):
    pass
admin.site.register(Day, DayAdmin)


class TimeRangeAdmin(admin.ModelAdmin):
    pass
admin.site.register(TimeRange, TimeRangeAdmin)

