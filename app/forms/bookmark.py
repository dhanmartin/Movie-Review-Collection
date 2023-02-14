from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from app.models.bookmark import (
    Bookmark,
    Bookmark_folder,
)


class Bookmark_folder_form(forms.ModelForm):
    class Meta:
        model = Bookmark_folder

        fields = (
            "user",
            "name",
        )

        error_messages = {
            "name": {"required": "Please provide a folder name."},
            NON_FIELD_ERRORS: {
                "unique_together": "Folder name already exists.",
            },
        }


class Bookmark_form(forms.ModelForm):
    class Meta:
        model = Bookmark

        fields = (
            "user",
            "folder",
            "data",
        )
