"""
Views for core app.
"""
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.views import View
from django.db.models import F

from .models import (
    Department, Faculty, StudyMaterial, UploadAudit, 
    TimetableEntry, SearchQueryLog, UserFavoriteMaterial, RecentlyViewedMaterial
)
from .forms import StudyMaterialUploadForm, StudyMaterialModerationForm


class HomeView(TemplateView):
    """Home page view showing departments and recent materials."""
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all().order_by("name")
        
        # Filter materials based on user permissions
        materials_queryset = StudyMaterial.objects.all()
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            materials_queryset = materials_queryset.filter(verification_status="approved")
        
        context["recent_materials"] = materials_queryset.order_by("-uploaded_at")[:5]
        return context


class DepartmentListView(ListView):
    """List view for all departments."""
    model = Department
    template_name = "core/department_list.html"
    context_object_name = "departments"
    paginate_by = 20
    ordering = ["name"]


class DepartmentDetailView(DetailView):
    """Detail view for a single department."""
    model = Department
    template_name = "core/department_detail.html"
    context_object_name = "department"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context["faculty_list"] = Faculty.objects.filter(
            department=department
        ).order_by("name")
        # Placeholders for later
        context["study_materials"] = []
        context["timetable_entries"] = []
        return context


class FacultyListView(ListView):
    """List view for all faculty with optional department filter."""
    model = Faculty
    template_name = "core/faculty_list.html"
    context_object_name = "faculty_list"
    ordering = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.GET.get("department")
        if department_id:
            try:
                department = get_object_or_404(Department, pk=department_id)
                queryset = queryset.filter(department=department)
            except (ValueError, Department.DoesNotExist):
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all().order_by("name")
        return context


class FacultyDetailView(DetailView):
    """Detail view for a single faculty member."""
    model = Faculty
    template_name = "core/faculty_detail.html"
    context_object_name = "faculty"


class StudyMaterialListView(ListView):
    """List view for study materials with filtering."""
    model = StudyMaterial
    template_name = "core/study_material_list.html"
    context_object_name = "materials"
    ordering = ["-uploaded_at"]

    def get_queryset(self):
        """Filter queryset based on query parameters and user permissions."""
        queryset = super().get_queryset()

        # Filter by verification status based on user permissions
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            queryset = queryset.filter(verification_status="approved")

        # Filter by department
        department_id = self.request.GET.get("department")
        if department_id:
            try:
                department = get_object_or_404(Department, pk=department_id)
                queryset = queryset.filter(department=department)
            except (ValueError, Department.DoesNotExist):
                pass

        # Filter by semester
        semester = self.request.GET.get("semester")
        if semester:
            try:
                queryset = queryset.filter(semester=int(semester))
            except (ValueError, TypeError):
                pass

        # Filter by year
        year = self.request.GET.get("year")
        if year:
            try:
                queryset = queryset.filter(year=int(year))
            except (ValueError, TypeError):
                pass

        # Track search query if any filters are applied
        has_filters = False
        search_parts = []

        if department_id:
            has_filters = True
            try:
                dept = Department.objects.get(pk=department_id)
                search_parts.append(f"department:{dept.short_code}")
            except (Department.DoesNotExist, ValueError):
                pass

        if semester:
            has_filters = True
            search_parts.append(f"semester:{semester}")

        if year:
            has_filters = True
            search_parts.append(f"year:{year}")

        # Log search query if filters were applied
        if has_filters:
            query_string = " ".join(search_parts)
            SearchQueryLog.objects.create(
                query=query_string,
                user=user if user.is_authenticated else None
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all().order_by("name")
        return context


class StudyMaterialDetailView(DetailView):
    """Detail view for a single study material."""
    model = StudyMaterial
    template_name = "core/study_material_detail.html"
    context_object_name = "material"
    
    def get_object(self, queryset=None):
        """Get the material object and increment views_count."""
        obj = super().get_object(queryset)
        # Increment views count
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        """Add favorite status and track recent view."""
        context = super().get_context_data(**kwargs)
        material = self.object
        user = self.request.user
        
        # Check if material is favorited by current user
        is_favorite = False
        if user.is_authenticated:
            is_favorite = UserFavoriteMaterial.objects.filter(
                user=user,
                material=material
            ).exists()
            
            # Track recent view
            RecentlyViewedMaterial.objects.update_or_create(
                user=user,
                material=material,
                defaults={'last_viewed_at': timezone.now()}
            )
        
        context['is_favorite'] = is_favorite
        return context


class StudyMaterialCreateView(LoginRequiredMixin, CreateView):
    """Create view for uploading study materials."""
    model = StudyMaterial
    form_class = StudyMaterialUploadForm
    template_name = "core/study_material_upload.html"
    success_url = reverse_lazy("material_list")

    def form_valid(self, form):
        """Set uploader, status, and create audit entry."""
        # Set the uploader to the current user
        form.instance.uploader_user = self.request.user
        # Set verification status to pending
        form.instance.verification_status = "pending"
        # uploaded_at will auto-default

        # Save the material
        response = super().form_valid(form)

        # Create audit entry
        UploadAudit.objects.create(
            material=self.object,
            uploader=self.request.user,
            action="upload",
            reason="Initial upload",
        )

        # Redirect to the detail page of the created material
        return redirect("material_detail", pk=self.object.pk)

    def get_success_url(self):
        """Redirect to the detail page of the created material."""
        return reverse_lazy("material_detail", kwargs={"pk": self.object.pk})


def is_verifier(user) -> bool:
    """Check if a user is a verifier."""
    if not user.is_authenticated:
        return False

    # Handle either default related_name or a custom one
    has_coordinator = False
    if hasattr(user, "coordinator_roles"):
        has_coordinator = user.coordinator_roles.exists()
    elif hasattr(user, "coordinator_set"):
        has_coordinator = user.coordinator_set.exists()

    return user.is_staff or user.is_superuser or has_coordinator


class StudyMaterialVerifierRequiredMixin(UserPassesTestMixin):
    """Mixin to require verifier permissions."""

    def test_func(self) -> bool:
        """Test if user is a verifier."""
        return is_verifier(self.request.user)

    def handle_no_permission(self):
        """Handle unauthorized access."""
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        return HttpResponseForbidden("You do not have permission to access this page.")


class StudyMaterialModerationListView(
    LoginRequiredMixin, StudyMaterialVerifierRequiredMixin, ListView
):
    """List view for moderation queue."""
    model = StudyMaterial
    template_name = "core/study_material_moderation_list.html"
    context_object_name = "materials"
    ordering = ["-uploaded_at"]

    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()

        # Filter by status
        status = self.request.GET.get("status", "pending")
        if status and status != "all":
            queryset = queryset.filter(verification_status=status)

        # Filter by department
        department_id = self.request.GET.get("department")
        if department_id:
            try:
                department = get_object_or_404(Department, pk=department_id)
                queryset = queryset.filter(department=department)
            except (ValueError, Department.DoesNotExist):
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all().order_by("name")
        context["current_status"] = self.request.GET.get("status", "pending")
        context["current_department_id"] = self.request.GET.get("department", "")
        return context


class StudyMaterialModerationDetailView(
    LoginRequiredMixin, StudyMaterialVerifierRequiredMixin, DetailView, FormMixin
):
    """Detail view for moderating a study material."""
    model = StudyMaterial
    template_name = "core/study_material_moderation_detail.html"
    context_object_name = "material"
    form_class = StudyMaterialModerationForm

    def get_success_url(self):
        """Redirect to moderation list after action."""
        return reverse_lazy("material_moderation_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.get_object()
        context["audit_logs"] = material.audit_logs.order_by("-timestamp")
        context["can_approve"] = is_verifier(self.request.user)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST request for moderation action."""
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        """Process the moderation action."""
        material = self.get_object()
        action = form.cleaned_data["action"]
        reason = form.cleaned_data.get("reason", "")

        # Update material based on action
        if action == "approve":
            material.verification_status = "approved"
            material.verifier = self.request.user
            material.verified_at = timezone.now()
        elif action == "reject":
            material.verification_status = "rejected"
            material.verifier = self.request.user
            material.verified_at = timezone.now()
        elif action == "request_changes":
            # Keep status as pending, but can update verifier
            material.verifier = self.request.user
            # verified_at stays None

        material.save()

        # Create audit entry
        UploadAudit.objects.create(
            material=material,
            uploader=self.request.user,
            action="edit",
            reason=reason if reason else f"Moderation action: {action}",
        )

        return redirect(self.get_success_url())


class TimetableListView(ListView):
    """List view for timetable entries with filtering."""
    model = TimetableEntry
    template_name = "core/timetable_list.html"
    context_object_name = "entries"
    paginate_by = 50
    ordering = ["date", "start_time"]

    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = TimetableEntry.objects.select_related("department", "instructor")
        today = timezone.now().date()

        # Filter by department
        department_id = self.request.GET.get("department")
        if department_id:
            try:
                department = get_object_or_404(Department, pk=department_id)
                queryset = queryset.filter(department=department)
            except (ValueError, Department.DoesNotExist):
                pass

        # Filter by semester
        semester = self.request.GET.get("semester")
        if semester:
            try:
                queryset = queryset.filter(semester=int(semester))
            except (ValueError, TypeError):
                pass

        # Filter by date
        date_str = self.request.GET.get("date")
        if date_str:
            try:
                from datetime import datetime

                filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(date=filter_date)
            except (ValueError, TypeError):
                pass
        else:
            # Default to upcoming entries (next 14 days)
            from datetime import timedelta

            end_date = today + timedelta(days=14)
            queryset = queryset.filter(date__gte=today, date__lte=end_date)

        return queryset.order_by("date", "start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all().order_by("name")
        context["current_department_id"] = self.request.GET.get("department", "")
        context["current_semester"] = self.request.GET.get("semester", "")
        context["current_date"] = self.request.GET.get("date", "")
        return context


class DepartmentTimetableView(TemplateView):
    """View for department-specific timetable."""
    template_name = "core/department_timetable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department_id = self.kwargs.get("department_id")

        # Get department or 404
        department = get_object_or_404(Department, pk=department_id)
        context["department"] = department

        # Get entries for this department
        entries = TimetableEntry.objects.filter(
            department=department
        ).select_related("instructor")

        # Filter by semester if provided
        semester = self.request.GET.get("semester")
        if semester:
            try:
                entries = entries.filter(semester=int(semester))
                context["selected_semester"] = int(semester)
            except (ValueError, TypeError):
                context["selected_semester"] = None
        else:
            context["selected_semester"] = None

        # Only show upcoming entries
        today = timezone.now().date()
        entries = entries.filter(date__gte=today).order_by("date", "start_time")

        context["entries"] = entries
        return context


class StudyMaterialDownloadView(DetailView):
    """View to track downloads and redirect to file."""
    model = StudyMaterial
    context_object_name = "material"
    
    def get(self, request, *args, **kwargs):
        """Increment download count and redirect to file."""
        material = self.get_object()
        
        # Increment downloads count
        material.downloads_count += 1
        material.save(update_fields=['downloads_count'])
        
        # Redirect to file_drive_id (Google Drive link or file)
        if material.file_drive_id:
            # If it's a URL, redirect to it
            if material.file_drive_id.startswith('http'):
                return redirect(material.file_drive_id)
            # Otherwise, construct Google Drive preview URL
            # Format: https://drive.google.com/file/d/{file_id}/view
            drive_url = f"https://drive.google.com/file/d/{material.file_drive_id}/view"
            return redirect(drive_url)
        
        # If no file_drive_id, redirect back to detail page
        return redirect('material_detail', pk=material.pk)


class TopMaterialsView(ListView):
    """View showing top materials by downloads and views."""
    model = StudyMaterial
    template_name = "core/analytics_top_materials.html"
    context_object_name = "materials"
    paginate_by = None  # No pagination, show all top 20
    
    def get_queryset(self):
        """Get top materials sorted by downloads + views + favorites."""
        queryset = StudyMaterial.objects.select_related('department').all()
        # Annotate with total engagement (favorites weighted 2x)
        queryset = queryset.annotate(
            total_engagement=F('downloads_count') + F('views_count') + F('favorites_count') * 2
        ).order_by('-total_engagement', '-downloads_count', '-views_count', '-favorites_count')
        return queryset[:20]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add rank numbers
        materials = list(context['materials'])
        for idx, material in enumerate(materials, start=1):
            material.rank = idx
        context['materials'] = materials
        return context


class SearchAnalyticsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """View showing search analytics."""
    template_name = "core/analytics_search_terms.html"
    context_object_name = "search_terms"
    paginate_by = 50
    
    def test_func(self):
        """Require staff or superuser access."""
        return self.request.user.is_staff or self.request.user.is_superuser
    
    def get_queryset(self):
        """Get top search queries with counts."""
        from django.db.models import Count, Max
        queryset = SearchQueryLog.objects.values('query').annotate(
            count=Count('id'),
            last_searched=Max('timestamp')
        ).order_by('-count', '-last_searched')[:50]
        return queryset


class ToggleFavoriteView(LoginRequiredMixin, View):
    """View to toggle favorite status for a study material."""
    http_method_names = ['post']
    
    def post(self, request, pk):
        """Toggle favorite status for the material."""
        material = get_object_or_404(StudyMaterial, pk=pk)
        user = request.user
        
        # Check if favorite already exists
        try:
            favorite = UserFavoriteMaterial.objects.get(user=user, material=material)
            # Favorite exists, remove it
            favorite.delete()
            # Decrement favorites_count (ensure it doesn't go below 0)
            StudyMaterial.objects.filter(pk=material.pk).update(
                favorites_count=F('favorites_count') - 1
            )
        except UserFavoriteMaterial.DoesNotExist:
            # Favorite doesn't exist, create it
            UserFavoriteMaterial.objects.create(user=user, material=material)
            # Increment favorites_count
            StudyMaterial.objects.filter(pk=material.pk).update(
                favorites_count=F('favorites_count') + 1
            )
        
        # Redirect back to material detail page
        return redirect('material_detail', pk=material.pk)


class MyLibraryView(LoginRequiredMixin, TemplateView):
    """View showing user's favorite and recently viewed materials."""
    template_name = "core/my_library.html"
    
    def get_context_data(self, **kwargs):
        """Get favorites and recent views for the current user."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Check if user is staff/superuser/verifier
        is_verifier_user = is_verifier(user)
        
        # Get favorites
        favorites_qs = UserFavoriteMaterial.objects.filter(
            user=user
        ).select_related('material', 'material__department').order_by('-created_at')
        
        # Get recent views
        recent_qs = RecentlyViewedMaterial.objects.filter(
            user=user
        ).select_related('material', 'material__department').order_by('-last_viewed_at')
        
        # Apply visibility rules for non-staff users
        if not is_verifier_user:
            favorites_qs = favorites_qs.filter(material__verification_status='approved')
            recent_qs = recent_qs.filter(material__verification_status='approved')
        
        # Limit to 20 items each
        context['favorite_entries'] = favorites_qs[:20]
        context['recent_entries'] = recent_qs[:20]
        
        return context
