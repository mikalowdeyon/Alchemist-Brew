from django import forms
from .models import Order, StudyRoomBooking, MenuItem

class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Order
        fields = ["items"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = StudyRoomBooking
        fields = ["date", "time_slot"]
