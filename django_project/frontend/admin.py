"""Admin page for Context Layer models."""
from celery.result import AsyncResult
from core.celery import app
from core.settings.utils import absolute_path
from django.contrib import admin, messages
from django.core.management import call_command
from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from frontend.models import (
    BoundaryFile,
    BoundarySearchRequest,
    ContextLayer,
    ContextLayerLegend,
    ContextLayerTilingTask,
    DraftSpeciesUpload,
    StatisticalModel,
    StatisticalModelOutput,
    Layer,
    MapSession,
    SpeciesModelOutput,
    UploadSpeciesCSV
)
from frontend.models.spatial import SpatialDataModel, SpatialDataValueModel
from frontend.tasks import (
    clear_older_vector_tiles,
    generate_vector_tiles_task,
    start_plumber_process,
    generate_species_statistical_model
)
from property.tasks import (
    generate_spatial_filter_for_all_properties
)


def cancel_other_processing_tasks(task_id=None):
    """Cancel any ongoing vector tile tasks."""
    tasks = ContextLayerTilingTask.objects.filter(
        status=ContextLayerTilingTask.TileStatus.PROCESSING
    )
    if task_id:
        tasks = tasks.exclude(id=task_id)
    for tiling_task in tasks:
        if tiling_task.task_id:
            res = AsyncResult(tiling_task.task_id)
            if not res.ready():
                app.control.revoke(
                    tiling_task.task_id,
                    terminate=True
                )
        tiling_task.task_id = None
        tiling_task.status = (
            ContextLayerTilingTask.TileStatus.CANCELLED
        )
        tiling_task.save()


@admin.action(description='Generate Vector Tile')
def generate_vector_tiles(modeladmin, request, queryset):
    cancel_other_processing_tasks()
    for tiling_task in queryset:
        if tiling_task.task_id:
            res = AsyncResult(tiling_task.task_id)
            if not res.ready():
                app.control.revoke(
                    tiling_task.task_id,
                    terminate=True
                )
        task = generate_vector_tiles_task.delay(tiling_task.id, True)
        tiling_task.task_id = task.id
        tiling_task.save()
    modeladmin.message_user(
        request,
        'Vector tile generation will be run in background!',
        messages.SUCCESS
    )


@admin.action(description='Resume Vector Tile Generation')
def resume_generate_vector_tiles(modeladmin, request, queryset):
    cancel_other_processing_tasks()
    for tiling_task in queryset:
        if tiling_task.task_id:
            res = AsyncResult(tiling_task.task_id)
            if not res.ready():
                app.control.revoke(
                    tiling_task.task_id,
                    terminate=True
                )
        task = generate_vector_tiles_task.delay(tiling_task.id, False)
        tiling_task.task_id = task.id
        tiling_task.save()
    modeladmin.message_user(
        request,
        'Vector tile generation will be run in background!',
        messages.SUCCESS
    )


@admin.action(description='Cancel Vector Tile Generation')
def cancel_generate_vector_tiles(modeladmin, request, queryset):
    for tiling_task in queryset:
        if tiling_task.task_id:
            res = AsyncResult(tiling_task.task_id)
            if not res.ready():
                app.control.revoke(
                    tiling_task.task_id,
                    terminate=True
                )
                tiling_task.task_id = None
                tiling_task.status = (
                    ContextLayerTilingTask.TileStatus.CANCELLED
                )
                tiling_task.save()
    modeladmin.message_user(
        request,
        'Vector tile task has been cancelled!',
        messages.SUCCESS
    )


@admin.action(description='Clear Vector Tile Directory')
def clear_vector_tiles(modeladmin, request, queryset):
    clear_older_vector_tiles.delay()
    modeladmin.message_user(
        request,
        'Vector tile directory will be cleared in background!',
        messages.SUCCESS
    )


class TilingTaskAdmin(admin.ModelAdmin):
    """Admin page for TilingTask model

    """
    list_display = ('status', 'started_at',
                    'finished_at', 'total_size')
    search_fields = [
        'status',
        'total_size',
        'started_at',
        'finished_at'
    ]
    actions = [generate_vector_tiles, resume_generate_vector_tiles,
               cancel_generate_vector_tiles, clear_vector_tiles]


class BoundaryFileAdmin(admin.ModelAdmin):
    """Admin page for BoundaryFile model

    """
    list_display = ('meta_id', 'name', 'upload_date', 'session', 'file_type')
    search_fields = [
        'name',
        'meta_id',
        'file_type',
        'upload_date',
        'session'
    ]


class BoundarySearchRequestAdmin(admin.ModelAdmin):
    """Admin page for BoundarySearchRequest model

    """
    list_display = ('session', 'type', 'status', 'progress')
    search_fields = [
        'session',
        'type',
        'status',
        'progress'
    ]


class ContextLayerAdmin(admin.ModelAdmin):
    """Admin page for ContextLayer model

    """
    change_list_template = "admin/context_layer.html"
    list_display = ('name', 'is_static')
    search_fields = ['name']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('reload_fixtures/', self.reload_fixtures,
                 name='reload-context-layer-fixtures'),
        ]
        return my_urls + urls

    def reload_fixtures(self, request):
        # delete
        ContextLayer.objects.all().delete()
        # load fixtures from json files
        call_command('loaddata', 'fixtures/context_layer.json',
                     app_label='frontend')
        call_command('loaddata', 'fixtures/context_layer_legend.json',
                     app_label='frontend')
        # reload Layer tables
        Layer.objects.all().delete()
        for context_layer in ContextLayer.objects.all():
            for layer_name in context_layer.layer_names:
                Layer.objects.create(name=layer_name,
                                     context_layer=context_layer)
        # once layer is created, need to patch spatial filter fields manually
        # before triggering patching spatial data job
        self.message_user(
            request,
            'Context layer fixtures has been successfully reloaded! '
            'Please trigger generate spatial filter from layer listing!',
            messages.SUCCESS
        )
        return HttpResponseRedirect('/admin/frontend/contextlayer/')


class ContextLayerLegendForm(ModelForm):
    class Meta:
        model = ContextLayerLegend
        fields = '__all__'
        widgets = {
            'colour': TextInput(attrs={'type': 'color'}),
        }


class ContextLayerLegendAdmin(admin.ModelAdmin):
    """Admin page for ContextLayerLegend model

    """
    list_display = ('name', 'layer', 'display_color')
    search_fields = [
        'name',
        'layer__name',
    ]
    form = ContextLayerLegendForm

    def display_color(self, obj):
        return format_html(
            '<span style="width:10px;height:10px;'
            'display:inline-block;background-color:%s"></span>' % obj.colour
        )
    display_color.short_description = 'Colour'
    display_color.allow_tags = True


class DraftSpeciesUploadAdmin(admin.ModelAdmin):
    """Admin page for DraftSpeciesUpload model

    """
    list_display = ('name', 'property', 'upload_by', 'taxon', 'year')
    search_fields = [
        'name',
        'property__name',
        'upload_by__username',
        'taxon__scientific_name',
        'year'
    ]


@admin.action(description='Restart plumber process')
def restart_plumber_process(modeladmin, request, queryset):
    start_plumber_process.apply_async(queue='plumber')
    modeladmin.message_user(
        request,
        'Plumber process will be started in background!',
        messages.SUCCESS
    )


class StatisticalModelOutputInline(admin.TabularInline):
    model = StatisticalModelOutput
    extra = 1


class StatisticalModelAdmin(admin.ModelAdmin):
    """Admin page for StatisticalModel model

    """
    change_form_template = "admin/statistical_model_change_form.html"
    list_display = ('taxon', 'name')
    search_fields = ['taxon__scientific_name', 'name']
    list_filter = ['taxon']
    actions = [restart_plumber_process]
    inlines = [StatisticalModelOutputInline]
    autocomplete_fields = ['taxon']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # disable taxon in edit mode
            # because SpeciesModelOutput depends on this
            return ['taxon']
        else:
            return []

    def response_change(self, request, obj):
        if '_download-data-template' in request.POST:
            template_file = absolute_path(
                'frontend', 'utils', 'data_sample.csv'
            )
            with open(template_file) as f:
                response = HttpResponse(
                    f.read(), content_type='text/csv'
                )
            response['Content-Disposition'] = (
                'attachment; filename="data_template.csv"'
            )
            return response
        return super().response_change(request, obj)


@admin.action(description='Trigger generate model output')
def trigger_generate_species_statistical_model(modeladmin, request, queryset):
    for output in queryset:
        task = generate_species_statistical_model.delay(output.id)
        output.task_id = task.id
        output.save(update_fields=['task_id'])
    modeladmin.message_user(
        request,
        'Generate statistical model output will be started in background!',
        messages.SUCCESS
    )


class SpeciesModelOutputAdmin(admin.ModelAdmin):
    """Admin page for Species Model Output."""
    list_display = ('taxon', 'model', 'is_latest', 'status',
                    'generated_on', 'is_outdated')
    search_fields = ['taxon__scientific_name', 'model__name']
    list_filter = ['taxon', 'model', 'is_latest', 'is_outdated']
    actions = [trigger_generate_species_statistical_model]


@admin.action(description='Trigger generate spatial filter')
def trigger_generate_spatial_filter(modeladmin, request, queryset):
    # check if there is at least one Layer with spatial_filter_field
    non_empty_layer = Layer.objects.exclude(
        spatial_filter_field__isnull=True
    ).exclude(spatial_filter_field__exact='')
    if non_empty_layer.count() == 0:
        modeladmin.message_user(
            request,
            'Please set spatial_filter_field to at least 1 layer object!',
            messages.WARNING
        )
        return
    generate_spatial_filter_for_all_properties.delay()
    modeladmin.message_user(
        request,
        'Generate spatial filter for all properties '
        'will be run in background!',
        messages.SUCCESS
    )


class LayerAdmin(admin.ModelAdmin):
    """Admin page for Layer model

    """
    list_display = (
        'name', 'context_layer', 'spatial_filter_field'
    )
    search_fields = [
        'name',
        'context_layer__name'
    ]
    actions = [trigger_generate_spatial_filter]


class SpatialDataValueModelAdmin(admin.StackedInline):
    """Admin page for SpatialDataValueMode model

    """
    list_display = (
        'spatial_data', 'layer', 'context_layer_value'
    )
    search_fields = [
        'spatial_data',
        'layer',
        'context_layer_value'
    ]
    model = SpatialDataValueModel


class SpatialDataModelAdmin(admin.ModelAdmin):
    """Admin page for SpatialDataModel model

    """
    list_display = (
        'property', 'context_layer'
    )
    search_fields = [
        'property__name',
        'context_layer__name'
    ]
    inlines = (
        SpatialDataValueModelAdmin,
    )


class MapSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'uuid', 'created_date', 'expired_date'
    )
    list_filter = ['user']


class UploadSpeciesCSVAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'uploader', 'property', 'uploaded_at'
    )
    list_filter = ['uploader']


admin.site.register(ContextLayer, ContextLayerAdmin)
admin.site.register(ContextLayerLegend, ContextLayerLegendAdmin)
admin.site.register(ContextLayerTilingTask, TilingTaskAdmin)
admin.site.register(BoundaryFile, BoundaryFileAdmin)
admin.site.register(BoundarySearchRequest, BoundarySearchRequestAdmin)
admin.site.register(DraftSpeciesUpload, DraftSpeciesUploadAdmin)
admin.site.register(StatisticalModel, StatisticalModelAdmin)
admin.site.register(SpatialDataModel, SpatialDataModelAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(MapSession, MapSessionAdmin)
admin.site.register(SpeciesModelOutput, SpeciesModelOutputAdmin)
admin.site.register(UploadSpeciesCSV, UploadSpeciesCSVAdmin)
