"""
URL configuration for core app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    path("departments/", views.DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/<int:pk>/",
        views.DepartmentDetailView.as_view(),
        name="department_detail",
    ),

    path("faculty/", views.FacultyListView.as_view(), name="faculty_list"),
    path(
        "faculty/<int:pk>/",
        views.FacultyDetailView.as_view(),
        name="faculty_detail",
    ),

    path("materials/", views.StudyMaterialListView.as_view(), name="material_list"),
    path(
        "materials/<int:pk>/",
        views.StudyMaterialDetailView.as_view(),
        name="material_detail",
    ),
    path(
        "materials/upload/",
        views.StudyMaterialCreateView.as_view(),
        name="material_upload",
    ),

    path(
        "materials/moderation/",
        views.StudyMaterialModerationListView.as_view(),
        name="material_moderation_list",
    ),
    path(
        "materials/moderation/<int:pk>/",
        views.StudyMaterialModerationDetailView.as_view(),
        name="material_moderation_detail",
    ),

    path("timetable/", views.TimetableListView.as_view(), name="timetable_list"),
    path(
        "timetable/department/<int:department_id>/",
        views.DepartmentTimetableView.as_view(),
        name="department_timetable",
    ),
    path(
        "materials/<int:pk>/download/",
        views.StudyMaterialDownloadView.as_view(),
        name="material_download",
    ),
    path(
        "materials/<int:pk>/favorite/",
        views.ToggleFavoriteView.as_view(),
        name="material_toggle_favorite",
    ),
    path(
        "analytics/top-materials/",
        views.TopMaterialsView.as_view(),
        name="analytics_top_materials",
    ),
    path(
        "analytics/search-terms/",
        views.SearchAnalyticsView.as_view(),
        name="analytics_search_terms",
    ),
    path(
        "library/",
        views.MyLibraryView.as_view(),
        name="my_library",
    ),
]
