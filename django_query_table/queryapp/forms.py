from django import forms
from .models import SQLQuery

class SQLQueryForm(forms.ModelForm):
    class Meta:
        model = SQLQuery
        fields = ['name', 'query']

class DatabaseForm(forms.Form):
    ENGINE_CHOICES = [
        ('django.db.backends.postgresql', 'PostgreSQL'),
        ('django.db.backends.mysql', 'MySQL'),
        ('django.db.backends.sqlite3', 'SQLite'),
    ]

    engine = forms.ChoiceField(choices=ENGINE_CHOICES)
    dbname = forms.CharField(max_length=100, help_text="Database name")
    user = forms.CharField(max_length=100, required=False, help_text="Database user (if applicable)")
    password = forms.CharField(max_length=100, required=False, help_text="Database password (if applicable)")
    host = forms.CharField(max_length=100, required=False, help_text="Database host (if applicable)")
    port = forms.CharField(max_length=5, required=False, help_text="Database port (if applicable)")
