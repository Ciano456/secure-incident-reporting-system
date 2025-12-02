"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: SECURE

Description:
This file defines all forms used to collect input from users in the secure
implementation of the application.

The secure branch focuses on:
- Consistent validation
- Preventing empty or malformed input
- Enforcing rules before data is saved
- Preparing input safely for use in the view layer

While Django provides built-in protection against many attacks (such as XSS
through automatic template escaping), validation at the form level ensures
that poor-quality or untrusted input is blocked as early as possible.
"""

from django import forms
from .models import Incident, Comment


class IncidentForm(forms.ModelForm):
    """
    Form for creating new incidents in the secure branch.

    Includes validation to prevent:
    - Empty titles
    - Extremely short descriptions
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

        # Styling handled via Tailwind CSS for consistent appearance
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
        Ensure titles are meaningful and not generic one-word values.
        """
        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_description(self):
        """
        Ensure enough detail is supplied.
        Insecure branch allows shorter values to demonstrate poor validation.
        """
        desc = self.cleaned_data.get("description", "").strip()
        if len(desc) < 20:
            raise forms.ValidationError("Description must be at least 20 characters long.")
        return desc


class CommentForm(forms.ModelForm):
    """
    Form used to submit comments.

    The secure version still trusts Django's built-in output escaping, while
    also ensuring comments are not empty or meaningless.
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
        Prevent empty or extremely short comment submissions.
        """
        body = self.cleaned_data.get("body", "").strip()
        if len(body) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters.")
        return body