from django.urls import path
from .views import page_not_found, forbidden

from .views import (
    IndexView,
    DishTypeListView,
    DishTypeDetailView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    CookListView,
    CookDetailView,
    CookCreateView,
    CookDeleteView,
)


urlpatterns = [
    path(
        "", IndexView.as_view(), name="index"
    ),
    path(
        "dish_types/", DishTypeListView.as_view(), name="dish-type-list"
    ),
    path(
        "dish_types/<int:pk>/",
        DishTypeDetailView.as_view(),
        name="dish-type-detail"
    ),
    path(
        "dish_types/create",
        DishTypeCreateView.as_view(),
        name="dish-type-create"
    ),
    path(
        "dish_types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish-type-update"
    ),
    path(
        "dish_types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish-type-delete"
    ),
    path(
        "dishes/", DishListView.as_view(), name="dish-list"
    ),
    path(
        "dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"
    ),
    path(
        "dishes/create/", DishCreateView.as_view(), name="dish-create"
    ),
    path(
        "dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"
    ),
    path(
        "dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"
    ),
    path(
        "cooks/", CookListView.as_view(), name="cook-list"
    ),
    path(
        "cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
    ),
    path(
        "cooks/create/", CookCreateView.as_view(), name="cook-create"
    ),
    path(
        "cooks/<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"
    ),
    path(
        "404/", page_not_found, name="404"
    ),
    path(
        "403/", forbidden, name="403"
    ),
]

app_name = "restaurant"
