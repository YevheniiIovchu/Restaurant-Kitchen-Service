from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class IsSuperUserMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IsStaffMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CookDetailIfIsStaffMixin(LoginRequiredMixin, generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        cook = self.get_object()

        if request.user == cook:
            return super().dispatch(request, *args, **kwargs)

        if not request.user.is_superuser:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
