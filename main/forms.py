from django import forms
from .models import Booking, Package, Blog
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['package', 'start_date', 'end_date', 'adults', 'children', 'preferred_package_type', 'special_requirements']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'min': 'today'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'min': 'today'}),
            'adults': forms.NumberInput(attrs={'min': 1}),
            'children': forms.NumberInput(attrs={'min': 0}),
            'special_requirements': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.package = kwargs.pop('package', None)
        super().__init__(*args, **kwargs)
        if self.package:
            self.fields['package'].initial = self.package
            self.fields['package'].widget = forms.HiddenInput()
            self.fields['adults'].widget.attrs['max'] = self.package.max_group_size

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now().date():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data.get('start_date')
        if start_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date.")
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        adults = cleaned_data.get('adults', 0)
        children = cleaned_data.get('children', 0)
        total_people = adults + children
        
        if self.package and total_people > self.package.max_group_size:
            raise forms.ValidationError(f"Maximum group size for this package is {self.package.max_group_size} people.")
        return cleaned_data

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'excerpt', 'featured', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent', 'rows': 3}),
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
        }