from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import last_12_months_choices
from ckeditor.fields import RichTextField
from django.urls import reverse
from src.car_rent.models import CarType


class Region(models.Model):
    name = models.CharField(_('Область'), max_length=100)
    img = models.ImageField(_('CategoriesSerializer'), upload_to='regions', null=True, blank=True)
    
    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name = _('Область')
        verbose_name_plural = _('Области')        


class Category(models.Model):
    name = models.CharField(_('Название'), max_length=200)
    img = models.ImageField(_('Изображение'), upload_to='cat_images', null=True, blank=True)
    region = models.ForeignKey(Region, verbose_name=_("Область"), on_delete=models.CASCADE, null=True, blank=True,
                               related_name='cats')

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name


class Prices(models.Model):
    STATUS_CHOICES = (
        (3, 'Завершено'),
        (2, 'Распроданно'),
        (1, 'Доступно')
    )
    
    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('KGS', 'KGS'),
        ('RUB', 'RUB'),
        ('KZT', 'KZT')
    )
    
    tour = models.ForeignKey('Tour', verbose_name=_('Тур'), on_delete=models.CASCADE, null=True, blank=True, related_name='prices')
    price = models.IntegerField(_('Цена'), null=True, blank=True)
    currency = models.CharField(_('Валюта'), max_length=5, choices=CURRENCY_CHOICES, default='USD')
    status = models.IntegerField(_('Статус'), choices=STATUS_CHOICES, default=1)
    deadline = models.DateField(_('Крайний срок'), null=True, blank=True)
    start = models.DateField(_('Начало тура'), null=True, blank=True)
    end = models.DateField(_('Конец тура'), null=True)

    def __str__(self):
        return str(self.price) or 'Price'

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


class Route(models.Model):
    tour = models.ForeignKey('Tour', verbose_name=_('Тур'), on_delete=models.SET_NULL, null=True, blank=True, related_name='routes')
    day = models.IntegerField(_('День'), null=True, blank=True)
    start = models.CharField(_('Начало (место)'), max_length=50, null=True, blank=True)
    finish = models.CharField(_('Конец (место)'), max_length=50, null=True, blank=True)
    description = RichTextField(_('Программа'), null=True, blank=True)
    hotel = models.CharField(_('Гостиница'), max_length=100, null=True, blank=True)
    meals = models.CharField(_('Питание'), max_length=100, null=True, blank=True)

    def __str__(self):
        return 'Route'

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'


class Images(models.Model):
    tour = models.ForeignKey('Tour', verbose_name=_('Тур'), on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    location = models.CharField(_('Место изображение'), max_length=100, null=True, blank=True)
    img = models.ImageField(_('Изображение'), upload_to='tour_images', null=True, blank=True)

    def __str__(self):
        return self.location or 'Image'


class TourReviews(models.Model):
    STATUS_CHOICES = (
        (1, 'Одобрено'),
        (0, 'Отказано'),
        (2, 'Не проверено'),
    )

    status = models.IntegerField(_('Статус'), choices=STATUS_CHOICES, default=2)
    tour = models.ForeignKey('Tour', verbose_name=_('Тур'), on_delete=models.CASCADE,
                             null=True, blank=True, related_name='reviews')
    rating = models.DecimalField(_('Рейтинг'), null=True, blank=True, max_digits=5, decimal_places=1)
    date = models.CharField(_('Посетил'), max_length=50, choices=last_12_months_choices(), null=True, blank=True)
    name = models.CharField(_('Имя'), max_length=100, null=True, blank=True)
    email = models.EmailField(_('Электронная почта'), max_length=100, null=True, blank=True)
    comment = models.TextField(_('Комментарий'), null=True, blank=True)
    date_created = models.DateField(_('Дата отзыва'), auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name or self.email or 'Review'

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
    

class TourRequest(models.Model):
    STATUS_CHOICES = (
        (1, _('Обслужено')),
        (0, _('Не обслужено')),
    )
    
    tour = models.ForeignKey('Tour', verbose_name=_('Тур'), on_delete=models.CASCADE, null=True, blank=True,
                                            related_name='TourRequest')
    status = models.IntegerField(_('Статус'), choices=STATUS_CHOICES, default=0)
    first_name = models.CharField(_('Имя'), max_length=100, null=True, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=100, null=True, blank=True)
    email = models.EmailField(_('Адрес электронной почты'), max_length=100, null=True, blank=True)
    phone = models.CharField(_('Телефон'), max_length=100, null=True, blank=True)
    comment = models.TextField(_('Комментарий'))
    price = models.ForeignKey('Prices', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(_('Дата запроса'), auto_now_add=True, null=True, blank=True)

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('Запрос на тур')
        verbose_name_plural = _('Запросы')    
            
            
class Tour(models.Model):
    TYPE_CHOICES = (
        (1, 'Гарантированный'),
        (2, 'По заявке'),
        (3, 'Предложить свой тур'),
    )

    title = models.CharField(_('Заголовок'), max_length=200, null=True, blank=True)
    cat = models.ForeignKey(Category, verbose_name=_('Категория'), on_delete=models.CASCADE, null=True, blank=True,
                            related_name='tours')
    type = models.IntegerField(_('Тип тура'), choices=TYPE_CHOICES, null=True, blank=True)
    duration = models.IntegerField(_('Продолжительность (день)'), null=True, blank=True)
    description = RichTextField(_('Описание'), null=True, blank=True)
    included = RichTextField(_('Включено'), null=True, blank=True)
    excluded = RichTextField(_('Не включено'), null=True, blank=True)
    top = models.BooleanField(_('Отображения в главной странице'), default=False)
    views = models.IntegerField(_('Просмотры'), default=0)

    class Meta:
        verbose_name = _('Тур')
        verbose_name_plural = _('Туры')

    def __str__(self):
        return self.title or 'Tour title'

    def get_absolute_url(self):
        return reverse('tour-detail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        self.included = self.included.replace('\r\n\r\n', '')
        self.excluded = self.excluded.replace('\r\n\r\n', '')
        self.description = self.description.replace('\r\n\r\n', '')
        super(Tour, self).save(*args, **kwargs)


class Slider(models.Model):
    title = models.CharField(_('Заголовок'), max_length=255, null=True, blank=True)
    subtitle = models.CharField(_('Подзаголовок'), max_length=255, null=True, blank=True)
    img = models.ImageField(_('Изображение'), upload_to='slider', null=True, blank=True)
    tour = models.OneToOneField(Tour, verbose_name=_('Тур на который ссылается слайдер'), on_delete=models.CASCADE,
                                null=True, blank=True)
    is_active = models.BooleanField(_('Активность'), default=False)

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'


class CreateOwnTour(models.Model):
    ACCOMMODATION_CHOICES = (
        ('Отель', 'Отель'),
        ('Юрта', 'Юрта'),
        ('Гостиница', 'Гостиница'),
        ('Палата', 'Палата'),
    )

    MEAT_CHOICES = (
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин'),
        ('Все включено','Все включено'),
    )

    PEOPLE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
    )

    METHOD_CHOICES = (
        ('Ватсапп', 'Ватсапп'),
        ('Звонки', 'Звонки'),
        ('Инстаграмм', 'Инстаграмм'),
        ('Телеграмм', 'Телеграмм'),
    )

    cat = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name=_('Категория'), null=True, blank=True)

    # Контактные данные
    name_tour = models.CharField(_('Название тура'), max_length=255, null=True, blank=True)
    accommodation = models.CharField(_('Жилье'), choices=ACCOMMODATION_CHOICES, max_length=100, null=True, blank=True)
    transport = models.ForeignKey(CarType, verbose_name=_('Транспорт'), on_delete=models.CASCADE, null=True, blank=True)
    meat = models.CharField(_('Питание'), choices=MEAT_CHOICES, max_length=100, null=True, blank=True)
    people = models.IntegerField(_('Кол-во людей'), choices=PEOPLE_CHOICES, null=True, blank=True)
    method = models.CharField(_('Способы связи'), choices=METHOD_CHOICES, max_length=100, null=True, blank=True)

    # Информация о путешествии
    comment = models.TextField(_('Комментарий и дополнительная информация'), null=True, blank=True)
    date_start = models.DateField(_('Дата начала'), null=True, blank=True)
    date_end = models.DateField(_('Дата окончания'), null=True, blank=True)

    def __str__(self):
        return self.name_tour

    class Meta:
        verbose_name = _('Создай свой тур')
        verbose_name_plural = _('Создайте свои туры')
        
