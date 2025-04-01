from django import forms
from .models import Booking, Package, Blog
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['package', 'travel_date', 'number_of_people', 'special_requests']
        widgets = {
            'travel_date': forms.DateInput(attrs={'type': 'date', 'min': 'today'}),
            'number_of_people': forms.NumberInput(attrs={'min': 1}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.package = kwargs.pop('package', None)
        super().__init__(*args, **kwargs)
        if self.package:
            self.fields['package'].initial = self.package
            self.fields['package'].widget = forms.HiddenInput()
            self.fields['number_of_people'].widget.attrs['max'] = self.package.max_group_size

    def clean_travel_date(self):
        travel_date = self.cleaned_data['travel_date']
        if travel_date < timezone.now().date():
            raise forms.ValidationError("Travel date cannot be in the past.")
        return travel_date

    def clean_number_of_people(self):
        number_of_people = self.cleaned_data['number_of_people']
        if self.package and number_of_people > self.package.max_group_size:
            raise forms.ValidationError(f"Maximum group size for this package is {self.package.max_group_size} people.")
        return number_of_people

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'excerpt', 'featured', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent', 'rows': 3}),
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
        } 