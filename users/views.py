from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
# Create your views here.
from .forms import *
from .models import *

# Реєстрація (взята готова з джанго)
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'

    # Контекст для шаблону
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реєстрація'
        return context

    def get_success_url(self):
        return reverse_lazy('login')

# Авторизація
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизація'
        return context

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('login')


# Профіль користувача
@login_required
def profile(request):
    user = request.user

    # Перевірка, чи існує опис профілю користувача. Якщо ні, створюємо його з значеннями за замовчуванням.
    user_profile, created = UserProfile.objects.get_or_create(user=user, defaults={'status': None, 'birth_date': None, 'workplace': None, 'wishes': None})

    user_news = News.objects.filter(author=user).order_by('-created_at')
    user_comments = Comment.objects.filter(user=user).order_by('-created_at')

    context = {
        'user_news': user_news,
        'user_comments': user_comments,
        'userprofile': user_profile,
    }
    return render(request, 'profile.html', context)


@login_required  # для перевірки, чи користувач залогінений
# Додавання новин
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('profile')
    else:
        form = NewsForm()

    context = {
        'form': form,
    }
    return render(request, 'news_form.html', context)


# Головна сторінка
def home(request):
    # Сортування новин за допомогою created_at (від нових до старих)
    all_news = News.objects.all().order_by('-created_at')

    # Сортування коментарів за допомогою created_at (від нових до старих)
    all_comments = Comment.objects.all().order_by('-created_at')

    context = {
        'all_news': all_news,
        'all_comments': all_comments,
    }
    return render(request, 'home.html', context)


@login_required
def add_like(request, news_id):
    # Отримуємо новину та власника новини
    news = get_object_or_404(News, pk=news_id)
    news_owner = news.author

    # Перевіряємо, чи користувач уже поставив лайк
    like, created = Like.objects.get_or_create(user=request.user, news=news)

    if not created:
        like.delete()

    if request.user != news_owner:
        # Створюємо повідомлення
        message = f"{request.user.username} вподобав вашу новину - {news}."
        Notification.objects.create(user=news_owner, message=message)

    return redirect(request.META.get('HTTP_REFERER'))


def add_comment(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    news_owner = news.author

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news
            comment.save()

            if request.user != news_owner:
                # Створюємо повідомлення
                message = f"{request.user.username} додав новий коментар до вашої новини: {news}"
                Notification.objects.create(user=news_owner, message=message)

        # Очистити дані форми, якщо коментар був успішно створений
        form = CommentForm()

    return redirect(request.META.get('HTTP_REFERER'))


# Для перегляду профілю іншого користувача
def user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # Якщо користувача не існує, відобразити повідомлення
        return HttpResponse("Користувача не знайдено")

    # Перевірка, чи користувач переглядає свій власний профіль
    if user == request.user:
        return redirect('profile')

    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        userprofile = None

    return render(request, 'user_profile.html', {'user': user, 'userprofile': userprofile})


# Повідомлення
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': user_notifications})



@login_required
# Редагування опису профілю користувача
def edit_user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправити на сторінку профілю після редагування
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
    }
    return render(request, 'user_profile_form.html', context)


# Редагування новини
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)

    if request.user == news.author:
        if request.method == 'POST':
            form = NewsForm(request.POST, instance=news)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = NewsForm(instance=news)
        return render(request, 'edit_news.html', {'form': form})


# Видалення новини
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)

    if request.user == news.author:
        news.delete()
        return redirect('profile')