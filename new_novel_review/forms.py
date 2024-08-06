from django import forms
from .models import Work, Scene, Post

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'creator']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'

class SceneForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = ['title', 'work']
    def __init__(self, *args, **kwargs):
        default_work = kwargs.pop('default_work', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'
        self.fields['work'].initial = default_work

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'work', 'hide']
    def __init__(self, *args, **kwargs):
        default_work = kwargs.pop('default_work', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'
        self.fields['work'].initial = default_work
