from django import forms
from django.contrib.auth.models import User
from django.forms import fields, widgets
from .models import Class, ClassCategory, MasterCategory, Post, SpecialSiteContent, WikiFile

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'category', 'master_category', 'short_description', 'content')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Post Titel',
                'type': 'text',
                'aira-describedby': 'titleValidationFeedback',
                'required': True
            }),
            # for manual falidation in class: {% if form.category.errors %}is-invalid{% else %}is-valid{% endif %}
            'category': forms.Select(attrs={
                'class': 'form-select',
                'aira-describedby': 'categoryValidationFeedback',
                'required': False
            }),
            'master_category': forms.Select(attrs={
                'class': 'form-select',
                'aira-describedby': 'masterCategoryValidationFeedback',
                'required': False
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Kurzbeschreibung des Posts',
                'aira-describedby': 'shortDescriptionValidationFeedback',
                'required': True,
                'rows': 4
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'aira-describedby': 'contentValidationFeedback',
                'required': True,
                'rows': 15
            })
        }


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'master_category', 'short_description', 'content')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Post Titel',
                'type': 'text',
                'required': True
            }),
            # for manual falidation in class: {% if form.category.errors %}is-invalid{% else %}is-valid{% endif %}
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': False
            }),
            'master_category': forms.Select(attrs={
                'class': 'form-select',
                'required': False
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Kurzbeschreibung des Posts',
                'required': True,
                'rows': 4
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'required': True,
                'rows': 15
            })
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control me-2',
        'type': 'search',
        'placeholder': 'Suche',
        'aria-label': 'Search'
    }))


class WikiFileForm(forms.Form):
    upload_file = forms.FileField(required=True, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'required': True
    }))


class ConnectPostWikiFileForm(forms.Form):
    # if only title in queryset than  .values_list('title', flat=True)
    post = forms.ModelChoiceField(queryset=Post.objects.all().order_by('post_date'), required=True, widget=forms.Select(attrs={
        'class': 'form-select',
        'required': True
    }))


class CategoryForm(forms.ModelForm):

    class Meta:
        model = ClassCategory
        fields = ('title', 'target_class')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Kategorie Titel',
                'type': 'text',
                'required': True
            }),
            'target_class': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }


class EditCategoryForm(forms.ModelForm):

    class Meta:
        model = ClassCategory
        fields = ('title', 'target_class')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Kategorie Titel',
                'type': 'text',
                'required': True
            }),
            # for manual falidation in class: {% if form.category.errors %}is-invalid{% else %}is-valid{% endif %}
            'target_class': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }

    
class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Klassen-Name',
                'type': 'text',
                'required': True
            }),
        }


class EditClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Klassen-Name',
                'type': 'text',
                'required': True
            }),
        }


class MasterCategoryForm(forms.ModelForm):

    class Meta:
        model = MasterCategory
        fields = ('title',)

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Haupt-Kategorie Titel',
                'type': 'text',
                'required': True
            }),
        }


class EditMasterCategoryForm(forms.ModelForm):

    class Meta:
        model = MasterCategory
        fields = ('title',)

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Haupt-Kategorie Titel',
                'type': 'text',
                'required': True
            }),
        }


class EditSpecialSiteContentForm(forms.ModelForm):

    class Meta:
        model = SpecialSiteContent
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Inhalt',
                'rows': 5
            }),
        }