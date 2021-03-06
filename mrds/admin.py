from django.contrib import admin

from mrds.models import State, County, Commodity, OperationType, DevelopmentStatus, WorkType, Site


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    search_fields = ('name', 'state')


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DevelopmentStatus)
class DevelopmentStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Site)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'dep_id', 'mrds_id', 'state', 'county', 'commodity_1', 'commodity_2', 'commodity_3')
    search_fields = ('site_name', 'dep_id', 'mrds_id', 'state__name', 'county__name', 'commodity_1__name',
                     'commodity_2__name', 'commodity_3__name')
