from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.models import Product, Record


# Create your views here.
class IndexView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Главная страница',
        'object_list': Product.objects.all()
    }


class ProductListView(ListView):
    model = Product
    extra_context = {
        'object_list': Product.objects.all(),
        'title': 'Все продукты'
    }


class RecordListView(ListView):
    model = Record
    extra_context = {
        'title': 'Все записи',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_publication=True)
        return queryset


class RecordDetailView(DetailView):
    model = Record

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        obj = self.get_object()
        increase = get_object_or_404(Record, pk=obj.pk)
        increase.increase_views()
        return context_data


class RecordCreateView(CreateView):
    model = Record
    fields = ('record_title', 'slug', 'content', 'preview')
    success_url = reverse_lazy('main:records_list')


class RecordUpdateView(UpdateView):
    model = Record
    fields = ('record_title', 'slug', 'content', 'preview')

    def get_success_url(self):
        return reverse('main:record_detail', args=[str(self.object.slug)])


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('main:records_list')


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class ContactView(TemplateView):
    template_name = 'main/contact.html'
    extra_context = {
        'title': 'Контакты'
    }

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if not name or not email or not message:
            context = {"error": "Введите все поля!"}
            return render(request, self.template_name, context=context)

        print(f'Сообщение от {name}({email}): {message}')

        context = {"success": "Сообщение успешно отправлено!"}
        return render(request, self.template_name, context=context)
