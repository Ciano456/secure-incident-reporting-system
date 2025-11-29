from django import forms
from .models import Incident, Comment


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            "title",
            "description",
            "category",
            "severity",
            "is_anonymous",
        ]
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
        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_description(self):
        desc = self.cleaned_data.get("description", "").strip()
        if len(desc) < 20:
            raise forms.ValidationError("Description must be at least 20 characters long.")
        return desc
    
class CommentForm(forms.ModelForm):
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
        body = self.cleaned_data.get("body", "").strip()
        if len(body) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters.")
        return body