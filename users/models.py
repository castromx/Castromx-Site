from django.db import models
from django.contrib.auth.models import User

# Унікальне поле "нікнейм" для користувача
User._meta.get_field('username')._unique = True

# Унікальне поле "емейл" для користувача
User._meta.get_field('email')._unique = True

# Таблиця для збереження новин
class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Публікація')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_news', blank=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)

    def __str__(self):
        return self.title

# Таблиця для збереження лайків
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Таблиця для збереження коментарів
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Таблиця для повідомлень
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

# Таблиця для опису профілю
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    workplace = models.CharField(max_length=100, blank=True, null=True)
    wishes = models.CharField(max_length=100, blank=True, null=True) # спочатку це було полем - бажання, так як я знав що треба буде ще одне поле
    # коли створював, зараз воно називається інше (для посилань на інші соц. мережі і тд)

    def __str__(self):
        return self.user.username

