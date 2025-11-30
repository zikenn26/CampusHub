"""
Admin configuration for core app models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Department, Faculty, StudyMaterial,
    UploadAudit, TimetableEntry, Notification, Coordinator, SearchQueryLog,
    UserFavoriteMaterial, RecentlyViewedMaterial
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    list_display = ['email', 'name', 'role', 'phone', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'name', 'phone']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('name', 'role', 'phone', 'telegram_id', 'whatsapp_number', 'created_at')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('name', 'role', 'phone', 'telegram_id', 'whatsapp_number')
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin configuration for Department model."""
    list_display = ['name', 'short_code', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'short_code']
    ordering = ['name']


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Admin configuration for Faculty model."""
    list_display = ['name', 'title', 'department', 'status', 'contact_email']
    list_filter = ['department', 'status']
    search_fields = ['name', 'title', 'contact_email']
    ordering = ['name']
    raw_id_fields = ['department']


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    """Admin configuration for StudyMaterial model."""
    list_display = [
        'title', 'department', 'downloads_count', 'views_count',
        'verification_status', 'uploaded_at'
    ]
    list_filter = [
        'department', 'file_type', 'verification_status',
        'semester', 'year', 'uploaded_at'
    ]
    search_fields = ['title', 'description', 'uploader_user__name', 'uploader_user__email']
    ordering = ['-uploaded_at']
    raw_id_fields = ['department', 'uploader_user', 'verifier']
    readonly_fields = ['uploaded_at', 'verified_at', 'downloads_count', 'views_count', 'thumbs_up_count', 'favorites_count']
    
    def get_queryset(self, request):
        """Optimize queryset for admin."""
        qs = super().get_queryset(request)
        return qs.select_related('department', 'uploader_user')


@admin.register(UploadAudit)
class UploadAuditAdmin(admin.ModelAdmin):
    """Admin configuration for UploadAudit model."""
    list_display = ['material', 'uploader', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['material__title', 'uploader__name', 'uploader__email', 'reason']
    ordering = ['-timestamp']
    raw_id_fields = ['material', 'uploader']
    readonly_fields = ['timestamp']


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    """Admin configuration for TimetableEntry model."""
    list_display = [
        'course_code', 'course_name', 'department', 'semester',
        'date', 'start_time', 'end_time', 'venue', 'instructor'
    ]
    list_filter = ['department', 'semester', 'date', 'instructor']
    search_fields = ['course_code', 'course_name', 'venue', 'instructor__name']
    ordering = ['date', 'start_time']
    raw_id_fields = ['department', 'instructor']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin configuration for Notification model."""
    list_display = [
        'title', 'department', 'created_by', 'sent_status',
        'scheduled_for', 'created_at'
    ]
    list_filter = ['department', 'sent_status', 'created_at', 'scheduled_for']
    search_fields = ['title', 'body', 'created_by__name', 'created_by__email']
    ordering = ['-created_at']
    raw_id_fields = ['department', 'created_by']
    readonly_fields = ['created_at']


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    """Admin configuration for Coordinator model."""
    list_display = ['user', 'department', 'role', 'contact_info']
    list_filter = ['department', 'role']
    search_fields = ['user__name', 'user__email', 'department__name', 'contact_info']
    ordering = ['department', 'role', 'user']
    raw_id_fields = ['user', 'department']


@admin.register(SearchQueryLog)
class SearchQueryLogAdmin(admin.ModelAdmin):
    """Admin configuration for SearchQueryLog model."""
    list_display = ['query', 'user', 'timestamp']
    list_filter = ['timestamp', 'user']
    search_fields = ['query', 'user__name', 'user__email']
    ordering = ['-timestamp']
    raw_id_fields = ['user']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(UserFavoriteMaterial)
class UserFavoriteMaterialAdmin(admin.ModelAdmin):
    """Admin configuration for UserFavoriteMaterial model."""
    list_display = ['user', 'material', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__name', 'user__email', 'material__title']
    ordering = ['-created_at']
    raw_id_fields = ['user', 'material']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(RecentlyViewedMaterial)
class RecentlyViewedMaterialAdmin(admin.ModelAdmin):
    """Admin configuration for RecentlyViewedMaterial model."""
    list_display = ['user', 'material', 'last_viewed_at']
    list_filter = ['last_viewed_at', 'user']
    search_fields = ['user__name', 'user__email', 'material__title']
    ordering = ['-last_viewed_at']
    raw_id_fields = ['user', 'material']
    readonly_fields = ['last_viewed_at']
    date_hierarchy = 'last_viewed_at'

