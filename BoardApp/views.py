from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import AdFilter
from .forms import AdForm
from .models import Ad


class AdList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Ad
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-ad_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 2  # количество записей на странице


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'


class AdCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('BoardApp.add_ad',)
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'ad_create.html'
    success_url = reverse_lazy('ad')

    def form_valid(self, form):
        ad = form.save(commit=False)
        if self.request.method == 'POST':
            ad.author = self.request.user
        ad.save()
        return super().form_valid(form)


class AdUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('BoardApp.change_ad',)
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'


class AdDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('BoardApp.delete_ad',)
    raise_exception = True
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('ad_list')
