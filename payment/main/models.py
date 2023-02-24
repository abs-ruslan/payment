from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    '''Модель Товар'''
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(validators=[MinValueValidator(1.0)], max_digits=8, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name


class Coupon(models.Model):
    '''Модель Скидочный купон'''
    coupon_code = models.CharField(max_length=50, verbose_name='Код')
    percent_off = models.DecimalField(validators=[MinValueValidator(0.0)], max_digits=3, decimal_places=1, verbose_name='Размер скидки')

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
        ordering = ['percent_off']

    def __str__(self):
        return str(self.percent_off) + '%'


class Order(models.Model):
    '''Модель Заказ'''
    items = models.ManyToManyField(Item, verbose_name='Товар')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_paid = models.BooleanField(default=False, verbose_name='Статус оплаты')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Купон')

    @property
    def amount(self):
        '''Сумма заказа'''
        return self.items.all().aggregate(models.Sum('price'))['price__sum']
    amount.fget.short_description = 'Сумма'

    @property
    def get_items(self):
        '''Список товаров'''
        return ", ".join([item.name for item in self.items.all()])
    get_items.fget.short_description = 'Список товаров'

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['id']