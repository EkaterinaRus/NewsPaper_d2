from django.contrib.auth import models
from news.models import Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import SignupView, LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView




@login_required
def upgrade_me(request):
    user = request.user
    authors_group = models.Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')


class MySignupView(SignupView):
    template_name = 'signup.html'


class MyLoginView(LoginView):
    template_name = 'login.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['subscribed_categories'] = Category.objects.filter(subscribers=user)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context



