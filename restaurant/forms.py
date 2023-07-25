from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from restaurant.models import Dish, Cook, DishType

MAX_EXPERIENCE = 60


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = "__all__"


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
        )

    def clean_years_of_experience(self):
        return validate_years_of_experience(
            self.cleaned_data["years_of_experience"]
        )


def validate_years_of_experience(years_of_experience):
    if years_of_experience > MAX_EXPERIENCE:
        raise ValidationError(
            f"Years of experience cannot be more than {MAX_EXPERIENCE}"
        )
    return years_of_experience


class SearchForm(forms.Form):
    search = "param"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.search] = forms.CharField(
            max_length=255,
            required=False,
            label="",
            widget=forms.TextInput(
                attrs={"placeholder": f"Search by {self.search}..."}
            ),
        )


class CookSearchForm(SearchForm):
    search = "username"


class DishTypeSearchForm(SearchForm):
    search = "name"


class DishSearchForm(SearchForm):
    search = "name"


class DishTypeFilterForm(forms.Form):
    dish_type = forms.ModelMultipleChoiceField(
        queryset=DishType.objects.all(),
        required=False,
        label="By dish type",
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check-input"}
        )
    )
