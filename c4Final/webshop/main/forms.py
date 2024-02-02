from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'advantages', 'disadvantages']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'rating': 'Your Rating', 
        }
        required = {
            'rating': True,  
            'text': False,  
            'advantages': False,
            'disadvantages': False,
        }
