from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    authorRating = models.FloatField(default=0.0)
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(Sum(postRating='postRating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(Sum(commentRatinng='commentRating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        # commentArticleRat = self.author.commentPost.comment_set.all().aggregate(Sum(commentRatinng='commentRating'))
        # cArticleRat = 0
        # cArticleRat += commentArticleRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f"{self.authorUser}"

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'
        ordering = ['id']


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    ARTICLE = 'AR'
    NEWS = 'NW'
    categoryType = models.CharField(max_length=2, choices=[(ARTICLE, 'статья'), (NEWS, 'новость')], default=ARTICLE)
    datetimeCreation = models.DateTimeField(auto_now_add=True)
    postTitle = models.CharField(max_length=255)
    postText = models.TextField()
    postRating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.postTitle}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return self.postText[:125] + ' ...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['datetimeCreation']


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} {self.category}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentDatetime = models.DateTimeField(auto_now_add=True)
    commentText = models.TextField()
    commentRating = models.FloatField(default=0.0)

    def __str__(self):
        return self.commentPost.author.authorUser.username

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

