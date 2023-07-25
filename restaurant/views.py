from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import View, generic
from django.shortcuts import render

from restaurant.forms import (
    CookCreationForm,
    CookSearchForm,
    DishSearchForm,
    DishTypeSearchForm,
    DishForm,
    DishTypeFilterForm
)
from restaurant.mixins import (
    IsStaffMixin,
    IsSuperUserMixin,
    CookDetailIfIsStaffMixin
)
from restaurant.models import Dish, DishType, Cook


class IndexView(View):
    template_name = "restaurant/index.html"

    def get(self, request):
        num_cooks = get_user_model().objects.count()
        num_dishes = Dish.objects.count()
        num_dish_types = DishType.objects.count()
        num_visits = request.session.get("num_visits", 0)
        request.session["num_visits"] = num_visits + 1

        context = {
            "num_cooks": num_cooks,
            "num_dishes": num_dishes,
            "num_dish_types": num_dish_types,
            "num_visits": num_visits + 1,
        }

        return render(request, self.template_name, context=context)


class CookListView(IsStaffMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = get_user_model().objects.all()
        else:
            queryset = get_user_model().objects.filter(is_superuser=False)

        form = CookSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class CookDetailView(CookDetailIfIsStaffMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes__dish_type")


class CookCreateView(IsSuperUserMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


# class CookUpdateView(IsSuperUserMixin, generic.UpdateView):
#     model = Cook
#     success_url = reverse_lazy("restaurant:cook-list")


class CookDeleteView(IsSuperUserMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("restaurant:cook-list")


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        dish_type_ids = self.request.GET.getlist("dish_type", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )

        context["dish_type_filter_form"] = DishTypeFilterForm(
            initial={"dish_type": dish_type_ids}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        form = DishSearchForm(self.request.GET)
        dish_type_ids = self.request.GET.getlist("dish_type")

        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        if dish_type_ids:
            queryset = queryset.filter(dish_type_id__in=dish_type_ids)

        return queryset


class DishDetailView(generic.DetailView):
    model = Dish


class DishCreateView(IsSuperUserMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("restaurant:dish-list")


class DishUpdateView(IsStaffMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("restaurant:dish-list")


class DishDeleteView(IsSuperUserMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("restaurant:dish-list")


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "restaurant/dish_type_list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class DishTypeDetailView(generic.DetailView):
    model = DishType
    context_object_name = "dish_type"
    template_name = "restaurant/dish_type_detail.html"


class DishTypeCreateView(IsSuperUserMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "restaurant/dish_type_form.html"
    success_url = reverse_lazy("restaurant:dish-type-list")


class DishTypeUpdateView(IsSuperUserMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "restaurant/dish_type_form.html"
    success_url = reverse_lazy("restaurant:dish-type-list")


class DishTypeDeleteView(IsSuperUserMixin, generic.DeleteView):
    model = DishType
    template_name = "restaurant/dish_type_confirm_delete.html"
    success_url = reverse_lazy("restaurant:dish-type-list")


def page_not_found(request, exception):
    return render(request, 'errors/404.html', status=404)


def forbidden(request, exception):
    return render(request, 'errors/403.html', status=403)
