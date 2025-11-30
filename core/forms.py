"""
Forms for core app.
"""
from django import forms
from .models import StudyMaterial, Department


class StudyMaterialUploadForm(forms.ModelForm):
    """Form for uploading study materials."""
    subject_tags = forms.CharField(
        required=False,
        help_text='Enter tags separated by commas (e.g., "Math, Algebra, Calculus")',
        widget=forms.TextInput(attrs={'placeholder': 'Comma-separated tags'})
    )
    
    class Meta:
        model = StudyMaterial
        fields = [
            'department',
            'title',
            'description',
            'file_type',
            'file_drive_id',
            'subject_tags',
            'semester',
            'year',
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'file_type': forms.Select(attrs={'class': 'form-control'}),
            'file_drive_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL or file ID (Google Drive integration coming soon)'
            }),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_subject_tags(self):
        """Parse comma-separated tags into a list."""
        # Get the value from cleaned_data (already cleaned by base CharField)
        tags_str = self.cleaned_data.get('subject_tags', '')
        
        # If empty or None, return empty list
        if not tags_str:
            return []
        
        # If it's already a list (shouldn't happen, but handle it), return as is
        if isinstance(tags_str, list):
            return tags_str
        
        # Ensure it's a string before splitting
        if not isinstance(tags_str, str):
            return []
        
        # Split by comma, strip whitespace, filter out empty strings
        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tags
    
    def save(self, commit: bool = True) -> StudyMaterial:
        """Save the form and convert subject_tags to list."""
        instance = super().save(commit=False)
        # Get the cleaned subject_tags (already converted to list by clean_subject_tags)
        tags = self.cleaned_data.get('subject_tags', [])
        # Ensure it's a list
        if not isinstance(tags, list):
            tags = []
        instance.subject_tags = tags
        if commit:
            instance.save()
        return instance


class StudyMaterialModerationForm(forms.Form):
    """Form for moderating study materials."""
    ACTION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('request_changes', 'Request changes'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Optional comment or reason for this action'
        }),
        help_text='Optional comment or reason'
    )

