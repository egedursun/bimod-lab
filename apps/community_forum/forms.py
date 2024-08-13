from django import forms
from .models import ForumPost, ForumComment


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your post content here...'}),
        }


class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your comment here...'}),
        }
