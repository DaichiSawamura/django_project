from django import forms
from catalog.models import Product, Version

words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class FormStyleMixin:
    def __int__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data in words:
            raise forms.ValidationError('Эти продукты запрещены')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if cleaned_data in words:
            raise forms.ValidationError('Эти продукты запрещены')

        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"
