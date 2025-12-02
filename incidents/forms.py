"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: INSECURE

Description:
This file defines all Django forms used by the incident reporting application.

Forms handle:
- Input validation
- Data cleaning
- Rendering HTML form fields

In the insecure branch, validation is limited to basic length checks only.
Security protections such as input sanitisation and output encoding are
handled in the secure branch instead.
"""

from django import forms
from .models import Incident, Comment


class IncidentForm(forms.ModelForm):
    """
    Form linked to the Incident model.

    Used when a user reports a new incident.
    Provides light validation to ensure forms are not submitted with
    extremely short or empty values.
    """

    class Meta:
        model = Incident
        fields = [
            "title",
            "description",
            "category",
            "severity",
            "is_anonymous",
        ]

        # Styling is handled via Tailwind CSS classes
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-slate-900 focus:outline-none focus:ring-1 focus:ring-slate-900",
                "placeholder": "Brief summary of the incident",
            }),
            "description": forms.Textarea(attrs={
                "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-slate-900 focus:outline-none focus:ring-1 focus:ring-slate-900",
                "rows": 5,
                "placeholder": "Provide a factual description of what happened, when, and who was involved.",
            }),
            "category": forms.Select(attrs={
                "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-slate-900 focus:outline-none focus:ring-1 focus:ring-slate-900",
            }),
            "severity": forms.Select(attrs={
                "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-slate-900 focus:outline-none focus:ring-1 focus:ring-slate-900",
            }),
            "is_anonymous": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-900",
            }),
        }

    def clean_title(self):
        """
        Prevent extremely short incident titles.
        """
        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_description(self):
        """
        Enforce a minimum description length.
        Does NOT filter HTML or scripts in the insecure branch.
        """
        desc = self.cleaned_data.get("description", "").strip()
        if len(desc) < 20:
            raise forms.ValidationError("Description must be at least 20 characters long.")
        return desc


class CommentForm(forms.ModelForm):
    """
    Form used to submit comments on an incident.
    """

    class Meta:
        model = Comment
        fields = ["body", "is_internal"]

        widgets = {
            "body": forms.Textarea(attrs={
                "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-slate-900 focus:outline-none focus:ring-1 focus:ring-slate-900",
                "rows": 3,
                "placeholder": "Add a comment or update on this incident...",
            }),
            "is_internal": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-900",
            }),
        }

    def clean_body(self):
        """
        Ensure comments are not empty.
        No script filtering in insecure branch.
        """
        body = self.cleaned_data.get("body", "").strip()
        if len(body) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters.")
        return body