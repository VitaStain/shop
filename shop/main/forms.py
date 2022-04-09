from django import forms
from django.core.exceptions import ValidationError

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body_review', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if int(rating) > 5 or int(rating) < 1:
            raise ValidationError('Оценка должна быть от 1 до 5')
        return rating
