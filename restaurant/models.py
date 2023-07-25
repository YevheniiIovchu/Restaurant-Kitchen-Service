from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from restaurant_service import settings


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.ForeignKey(
        to=DishType,
        related_name="dishes",
        on_delete=models.CASCADE
    )
    cooks = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="dishes"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dishes"

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("restaurant:cook-detail", kwargs={"pk": self.pk})
