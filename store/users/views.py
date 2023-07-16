from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView

from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Регистрация прошла успешно!'
    title = 'Store - Регистрация'

    # def get_context_data(self, **kwargs):
    #    context = super(UserRegistrationView, self).get_context_data()
    #    context['title'] = 'Store - Регистрация'
    #    return context


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #    context = super(UserProfileView, self).get_context_data()
    #    context['basket'] = Basket.objects.filter(user=self.object)
    #    return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


# def login(request):
#    if request.method == 'POST':
#        form = UserLoginForm(data=request.POST)
#        if form.is_valid():
#            username = request.POST['username']
#            password = request.POST['password']
#            user = auth.authenticate(username=username, password=password)
#            if user:
#                auth.login(request, user)
#                return HttpResponseRedirect(reverse('index'))
#    else:
#        form = UserLoginForm()
#    context = {'form': form}
#    return render(request, 'users/login.html', context)


# def register(request):
#    if request.method == 'POST':
#        form = UserRegistrationForm(data=request.POST)
#        if form.is_valid():
#            form.save()
#            messages.success(request, 'Регистрация прошла успешно!')
#            return HttpResponseRedirect(reverse('users:login'))
#        else:
#            messages.error(request, 'Ошибка регистрации')
#    else:
#        form = UserRegistrationForm()
#    context = {'form': form}
#    return render(request, 'users/register.html', context)


# @login_required
# def profile(request):
#    if request.method == 'POST':
#        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect(reverse('users:profile'))
#        else:
#            print(form.errors)
#    else:
#        form = UserProfileForm(instance=request.user)
#    basket = Basket.objects.filter(user=request.user)
#    context = {'title': 'Store - Профиль',
#               'form': form,
#               'basket': basket,
#               }
#    return render(request, 'users/profile.html', context)


# def logout(request):
#    auth.logout(request)
#    return HttpResponseRedirect(reverse('index'))
