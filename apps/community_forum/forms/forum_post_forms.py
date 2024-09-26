from django import forms

from apps.community_forum.models import ForumPost


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your post content here...'}),
        }
