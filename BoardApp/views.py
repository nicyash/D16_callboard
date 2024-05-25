from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect


from .forms import AdForm, UserResponseForm, UserResponseAcceptForm
from .models import Ad, UserResponse
from .filters import AdFilter, UserResponseFilter


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

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = AdFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class UserResponseList(LoginRequiredMixin, ListView):
    model = UserResponse
    ordering = '-response_time'
    template_name = 'response.html'
    context_object_name = 'responses'
    paginate_by = 2

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = UserResponse.objects.filter(ad__author__id=self.request.user.id)
        self.filterset = UserResponseFilter(self.request.GET, queryset, request=self.request.user.id)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


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
    success_url = reverse_lazy('ad')


class UserResponseCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = UserResponseForm
    model = UserResponse
    template_name = 'response_create.html'
    success_url = reverse_lazy('ad')

    def form_valid(self, form):
        response = form.save(commit=False)
        if self.request.method == 'POST':
            response.author = self.request.user
            response.ad_id = self.kwargs['pk']
        response.save()
        return super().form_valid(form)


class UserResponseDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = UserResponse
    template_name = 'response_delete.html'
    success_url = reverse_lazy('response')


class UserResponseAccept(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = UserResponseAcceptForm
    model = UserResponse
    template_name = 'response_edit.html'
    success_url = reverse_lazy('response')

    def post(self, request, pk, **kwargs):
        if request.method == 'POST':
            response = UserResponse.objects.get(id=pk)
            response.status = True
            response.save()
            return redirect(f'response')
        else:
            return redirect(f'response')
