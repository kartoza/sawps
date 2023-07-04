"""Admin page for Context Layer models."""
from django.contrib import admin, messages
from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.utils.html import format_html
from celery.result import AsyncResult
from core.celery import app
from frontend.models import (
    ContextLayer,
    ContextLayerTilingTask,
    BoundaryFile,
    BoundarySearchRequest,
    ContextLayerLegend
)
from frontend.tasks import (
    generate_vector_tiles_task,
    clear_older_vector_tiles
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
    list_display = ('status', 'started_at',
                    'finished_at', 'total_size')
    actions = [generate_vector_tiles, resume_generate_vector_tiles,
               cancel_generate_vector_tiles, clear_vector_tiles]


class BoundaryFileAdmin(admin.ModelAdmin):
    list_display = ('meta_id', 'name', 'upload_date', 'session', 'file_type')


class BoundarySearchRequestAdmin(admin.ModelAdmin):
    list_display = ('session', 'type', 'status', 'progress')


class ContextLayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_static')


class ContextLayerLegendForm(ModelForm):
    class Meta:
        model = ContextLayerLegend
        fields = '__all__'
        widgets = {
            'colour': TextInput(attrs={'type': 'color'}),
        }


class ContextLayerLegendAdmin(admin.ModelAdmin):
    list_display = ('name', 'layer', 'display_color')
    form = ContextLayerLegendForm

    def display_color(self, obj):
        return format_html(
            '<span style="width:10px;height:10px;'
            'display:inline-block;background-color:%s"></span>' % obj.colour
        )
    display_color.short_description = 'Colour'
    display_color.allow_tags = True


admin.site.register(ContextLayer, ContextLayerAdmin)
admin.site.register(ContextLayerLegend, ContextLayerLegendAdmin)
admin.site.register(ContextLayerTilingTask, TilingTaskAdmin)
admin.site.register(BoundaryFile, BoundaryFileAdmin)
admin.site.register(BoundarySearchRequest, BoundarySearchRequestAdmin)
