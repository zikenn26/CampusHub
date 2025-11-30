"""
Core models for campus_hub application.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Email is used as the main login identifier.
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('cr', 'Class Representative'),
        ('faculty', 'Faculty'),
        ('authority', 'Authority'),
        ('moderator', 'Moderator'),
    ]
    
    name = models.CharField(
        max_length=150,
        verbose_name='Full Name',
        help_text='Enter your full name'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email Address',
        help_text='Your email address (used for login)'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name='Role',
        help_text='Your role in the system'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Phone Number',
        help_text='Your contact phone number'
    )
    telegram_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Telegram ID',
        help_text='Your Telegram username or ID'
    )
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='WhatsApp Number',
        help_text='Your WhatsApp number'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created At'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"{self.name} ({self.email})"


class Department(models.Model):
    """Department model representing academic departments."""
    name = models.CharField(
        max_length=200,
        verbose_name='Department Name',
        help_text='Full name of the department'
    )
    short_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Short Code',
        help_text='Short code for the department (e.g., CSE, ECE)'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description',
        help_text='Description of the department'
    )
    contact_emails = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Contact Emails',
        help_text='List of contact email addresses for the department'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created At'
    )
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']
        indexes = [
            models.Index(fields=['short_code']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} ({self.short_code})"


class Faculty(models.Model):
    """Faculty model representing faculty members."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('retired', 'Retired'),
    ]
    
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='faculty_members',
        verbose_name='Department'
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Name',
        help_text='Full name of the faculty member'
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Title',
        help_text='Academic title (e.g., Professor, Associate Professor)'
    )
    photo_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Photo URL',
        help_text='URL to the faculty member\'s photo'
    )
    biography = models.TextField(
        blank=True,
        null=True,
        verbose_name='Biography',
        help_text='Biography of the faculty member'
    )
    research_interests = models.TextField(
        blank=True,
        null=True,
        verbose_name='Research Interests',
        help_text='Research interests and areas of expertise'
    )
    contact_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Contact Email',
        help_text='Contact email address'
    )
    office_hours = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Office Hours',
        help_text='Office hours information'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Phone Number',
        help_text='Contact phone number'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Status'
    )
    
    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculty'
        ordering = ['name']
        indexes = [
            models.Index(fields=['department', 'status']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} - {self.department.short_code}"


class StudyMaterial(models.Model):
    """Study material model for uploaded study resources."""
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('link', 'Link'),
    ]
    
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='study_materials',
        verbose_name='Department'
    )
    uploader_user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='uploaded_materials',
        verbose_name='Uploader'
    )
    title = models.CharField(
        max_length=300,
        verbose_name='Title',
        help_text='Title of the study material'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description',
        help_text='Description of the study material'
    )
    file_drive_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='File Drive ID',
        help_text='Google Drive file ID'
    )
    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        verbose_name='File Type',
        help_text='Type of the study material'
    )
    subject_tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Subject Tags',
        help_text='List of subject tags for categorization'
    )
    semester = models.IntegerField(
        verbose_name='Semester',
        help_text='Semester number'
    )
    year = models.IntegerField(
        verbose_name='Year',
        help_text='Academic year'
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending',
        verbose_name='Verification Status'
    )
    verifier = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='verified_materials',
        verbose_name='Verifier'
    )
    uploaded_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Uploaded At'
    )
    verified_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Verified At'
    )
    downloads_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Downloads Count'
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Views Count'
    )
    thumbs_up_count = models.IntegerField(
        default=0,
        verbose_name='Thumbs Up Count'
    )
    favorites_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Favorites Count',
        help_text='Number of users who favorited this material'
    )
    
    class Meta:
        verbose_name = 'Study Material'
        verbose_name_plural = 'Study Materials'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['department', 'semester', 'year']),
            models.Index(fields=['verification_status']),
            models.Index(fields=['uploader_user']),
        ]
    
    def __str__(self) -> str:
        return f"{self.title} - {self.department.short_code}"


class UploadAudit(models.Model):
    """Audit log for study material uploads, edits, and deletions."""
    ACTION_CHOICES = [
        ('upload', 'Upload'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    ]
    
    material = models.ForeignKey(
        StudyMaterial,
        on_delete=models.CASCADE,
        related_name='audit_logs',
        verbose_name='Study Material'
    )
    uploader = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='audit_actions',
        verbose_name='User'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='Action'
    )
    reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='Reason',
        help_text='Reason for the action'
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name='Timestamp'
    )
    
    class Meta:
        verbose_name = 'Upload Audit'
        verbose_name_plural = 'Upload Audits'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['material', 'timestamp']),
            models.Index(fields=['uploader', 'timestamp']),
        ]
    
    def __str__(self) -> str:
        return f"{self.action} - {self.material.title} by {self.uploader.name}"


class TimetableEntry(models.Model):
    """Timetable entry model for class schedules."""
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='timetable_entries',
        verbose_name='Department'
    )
    semester = models.IntegerField(
        verbose_name='Semester',
        help_text='Semester number'
    )
    course_code = models.CharField(
        max_length=20,
        verbose_name='Course Code',
        help_text='Course code (e.g., CS101)'
    )
    course_name = models.CharField(
        max_length=200,
        verbose_name='Course Name',
        help_text='Full name of the course'
    )
    date = models.DateField(
        verbose_name='Date',
        help_text='Date of the class'
    )
    start_time = models.TimeField(
        verbose_name='Start Time',
        help_text='Class start time'
    )
    end_time = models.TimeField(
        verbose_name='End Time',
        help_text='Class end time'
    )
    venue = models.CharField(
        max_length=100,
        verbose_name='Venue',
        help_text='Class venue or room number'
    )
    instructor = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='timetable_entries',
        verbose_name='Instructor'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description',
        help_text='Additional description or notes'
    )
    
    class Meta:
        verbose_name = 'Timetable Entry'
        verbose_name_plural = 'Timetable Entries'
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(fields=['department', 'semester', 'date']),
            models.Index(fields=['date', 'start_time']),
        ]
    
    def __str__(self) -> str:
        return f"{self.course_code} - {self.date} {self.start_time}"


class Notification(models.Model):
    """Notification model for system notifications."""
    PUSH_TO_CHOICES = [
        ('email', 'Email'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('web', 'Web'),
    ]
    
    SENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name='Title',
        help_text='Notification title'
    )
    body = models.TextField(
        verbose_name='Body',
        help_text='Notification body content'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='notifications',
        verbose_name='Department',
        help_text='Leave blank for all departments'
    )
    push_to = models.JSONField(
        default=list,
        verbose_name='Push To',
        help_text='List of channels to push notification (email, telegram, whatsapp, web)'
    )
    created_by = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='created_notifications',
        verbose_name='Created By'
    )
    scheduled_for = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Scheduled For',
        help_text='Schedule notification for a specific date and time'
    )
    sent_status = models.CharField(
        max_length=20,
        choices=SENT_STATUS_CHOICES,
        default='pending',
        verbose_name='Sent Status'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created At'
    )
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['department', 'sent_status']),
            models.Index(fields=['scheduled_for', 'sent_status']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self) -> str:
        dept = self.department.short_code if self.department else 'All'
        return f"{self.title} - {dept} ({self.sent_status})"


class Coordinator(models.Model):
    """Coordinator model for class representatives and coordinators."""
    ROLE_CHOICES = [
        ('cr', 'Class Representative'),
        ('coordinator', 'Coordinator'),
    ]
    
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='coordinator_roles',
        verbose_name='User'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='coordinators',
        verbose_name='Department'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name='Role'
    )
    contact_info = models.TextField(
        blank=True,
        null=True,
        verbose_name='Contact Info',
        help_text='Additional contact information'
    )
    
    class Meta:
        verbose_name = 'Coordinator'
        verbose_name_plural = 'Coordinators'
        ordering = ['department', 'role', 'user']
        indexes = [
            models.Index(fields=['department', 'role']),
        ]
        unique_together = [['user', 'department', 'role']]
    
    def __str__(self) -> str:
        return f"{self.user.name} - {self.get_role_display()} ({self.department.short_code})"


class SearchQueryLog(models.Model):
    """Model to track search queries for analytics."""
    query = models.CharField(
        max_length=255,
        verbose_name='Search Query',
        help_text='The search query entered by the user'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_queries',
        verbose_name='User',
        help_text='User who performed the search (if authenticated)'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Timestamp'
    )
    
    class Meta:
        verbose_name = 'Search Query Log'
        verbose_name_plural = 'Search Query Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self) -> str:
        user_str = self.user.name if self.user else 'Anonymous'
        return f"{self.query} - {user_str} ({self.timestamp})"


class UserFavoriteMaterial(models.Model):
    """Model to track user favorite study materials."""
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='favorite_materials',
        verbose_name='User',
        help_text='User who favorited this material'
    )
    material = models.ForeignKey(
        StudyMaterial,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Study Material',
        help_text='The study material that was favorited'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
        help_text='When this material was favorited'
    )
    
    class Meta:
        verbose_name = 'User Favorite Material'
        verbose_name_plural = 'User Favorite Materials'
        ordering = ['-created_at']
        unique_together = [['user', 'material']]
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['material']),
        ]
    
    def __str__(self) -> str:
        return f"{self.user.name} favorited {self.material.title}"


class RecentlyViewedMaterial(models.Model):
    """Model to track recently viewed study materials by users."""
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='recently_viewed_materials',
        verbose_name='User',
        help_text='User who viewed this material'
    )
    material = models.ForeignKey(
        StudyMaterial,
        on_delete=models.CASCADE,
        related_name='recent_views',
        verbose_name='Study Material',
        help_text='The study material that was viewed'
    )
    last_viewed_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Viewed At',
        help_text='When this material was last viewed by the user'
    )
    
    class Meta:
        verbose_name = 'Recently Viewed Material'
        verbose_name_plural = 'Recently Viewed Materials'
        ordering = ['-last_viewed_at']
        unique_together = [['user', 'material']]
        indexes = [
            models.Index(fields=['user', '-last_viewed_at']),
            models.Index(fields=['-last_viewed_at']),
            models.Index(fields=['material']),
        ]
    
    def __str__(self) -> str:
        return f"{self.user.name} viewed {self.material.title} at {self.last_viewed_at}"

