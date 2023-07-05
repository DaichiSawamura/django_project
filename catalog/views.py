from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Record, Category, Version
from catalog.services import get_category_subjects


# Create your views here.
class IndexView(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Главная страница',
        'object_list': Product.objects.all()
    }


class CategoriesListView(ListView):
    model = Category
    extra_context = {
        'title': 'Все категории',
        'object_list': Category.objects.all()
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['subject_list'] = get_category_subjects
        return context_data


class ProductListView(ListView):
    model = Product
    extra_context = {
        'object_list': Product.objects.filter(status='Активна'),
        'version_list': Version.objects.filter(sign_of_publication=True),
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
    success_url = reverse_lazy('catalog:records_list')


class RecordUpdateView(UpdateView):
    model = Record
    fields = ('record_title', 'slug', 'content', 'preview')

    def get_success_url(self):
        return reverse('catalog:record_detail', args=[str(self.object.slug)])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('catalog:records_list')


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form_with_formset.html'
    success_url = reverse_lazy('catalog:products_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST)
        else:
            context_data['formset'] = SubjectFormset()
        return context_data


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')


class VersionListView(ListView):
    model = Version
    extra_context = {
        'object_list': Version.objects.filter(sign_of_publication=True),
        'title': 'Все версии'
    }


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:products_list')


class VersionDetailView(DetailView):
    model = Version

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'
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
