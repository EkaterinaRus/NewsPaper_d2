from datetime import datetime
from pydoc import resolve

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache



class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML,
    # в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id')
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# создаём представление, в котором будут детали конкретного отдельного товара
class PostDetail(DetailView):
    # template_name = 'newsdetail.html'
    # queryset = Post.objects.all()

    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'newsdetail.html'  # название шаблона будет product.html
    context_object_name = 'newsdetail'  # название объекта

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostSearchList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML,
    # в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id')
    paginate_by = 3

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data
        # у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр вконтекст
        return context


class PostAddView(PermissionRequiredMixin, CreateView):
    template_name = 'news_add.html'
    form_class = PostForm
    permission_required = ('news.add_post', )


class PostEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news_add.html'
    form_class = PostForm
    permission_required = ('news.change_post', )

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news_delete.html'  # название шаблона будет product.html
    context_object_name = 'newsdetail'
    success_url = '/news/'

class CategoryDetailView(DetailView):
    model = Category  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'category.html'  # название шаблона будет product.html
    context_object_name = 'category'  # название объекта

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = self.get_object()
        context['news'] = category.post_set.all()
        context['subscribed'] = category.subscribers.filter(username=user.username).exists()
        # sibscribed = category.subscribers.filter(email=user.email)
        # if not sibscribed:
        #     context['category'] = category
        return context

def email_success(request):
    res = 'Email is verified!'
    return HttpResponse('<p>%s</p>' % res)

# class AppointmentView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'make_appointment.html', {})
#
#     def post(self, request, *args, **kwargs):
#         appointment = Post(
#             client_name=request.POST['postTitle'],
#         )
#         appointment.save()
#
#         return redirect('appointments:make_appointment')


# class PostCategoryView(ListView):
#     model = Post
#     template_name = 'category.html'
#     context_object_name = 'news'
#     queryset = Post.objects.order_by('-id')
#     paginate_by = 3
#
#     def get_queryset(self):
#         self.id = resolve(self.request.path_info).kwargs['pk']
#         c = Category.objects.get(id=self.id)
#         queryset = Post.objects.filter(category=c)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         category = Category.objects.get(id=self.id)
#         sibscribed = category.subscribers.filter(email=user.email)
#         if not sibscribed:
#             context['category'] = category
#         return context

@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'categories': category,
                'user': user,
            },
        )

        msg = EmailMultiAlternatives(
            subject='Уведомление о подписке',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)

    return redirect('/sign')

# def subscribe_to_category(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#
#     if not category.subscribers.filter(id=user.id).exists():
#         category.subscribers.add(user)
#         html = render_to_string(
#             'email/subscribed.html',
#             {
#                 'categories': category,
#                 'user': user,
#             },
#         )
#
#         msg = EmailMultiAlternatives(
#             subject=f'{category} subsription',
#             body='',
#             from_email='peterbadson@yandex.ru',
#             to=['skavik46111@gmail.com'],  # это то же, что и recipients_list
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#
#         msg.send()  # отсылаем



