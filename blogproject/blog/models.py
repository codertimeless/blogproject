
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import strip_tags

import markdown


# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '分类'
		verbose_name_plural = verbose_name


class Tag(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '标签'
		verbose_name_plural = verbose_name


class Post(models.Model):
	title = models.CharField('标题', max_length=70)
	body = models.TextField('正文')
	created_time = models.DateTimeField('创建时间', auto_now_add=True)
	modified_time = models.DateTimeField('修改时间', auto_now=True)
	excerpt = models.CharField('摘要', max_length=200, blank=True)
	category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
	author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = '文章'
		verbose_name_plural = verbose_name

	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
		])

		self.excerpt = strip_tags(md.convert(self.body))[:54]

		super().save(*args, **kwargs)