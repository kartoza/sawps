"""Admin page for Context Layer models."""
from django.contrib import admin, messages
from celery.result import AsyncResult
from core.celery import app
from frontend.models import ContextLayer, ContextLayerTilingTask
from frontend.tasks import generate_vector_tiles_task


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


class TilingTaskAdmin(admin.ModelAdmin):
    list_display = ('status', 'started_at',
                    'finished_at', 'total_size')
    actions = [generate_vector_tiles, resume_generate_vector_tiles,
               cancel_generate_vector_tiles]


admin.site.register(ContextLayer)
admin.site.register(ContextLayerTilingTask, TilingTaskAdmin)
