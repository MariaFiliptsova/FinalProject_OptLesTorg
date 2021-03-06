from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class CategoryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_side_bar(self):
        models = get_models_for_count('vagonka', 'terrace')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url())
            for c in qs
        ]
        return data


class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'


    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение', null=True,
                              blank=True)
    description = models.TextField(max_length=1000, verbose_name='Описание',
                                   null=True, blank=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                verbose_name='Стоимость')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class Vagonka(Product):

    class Meta:
        verbose_name = 'Вагонка'
        verbose_name_plural = 'Вагонка'

    depth = models.CharField(max_length=20, verbose_name='Толщина')
    width = models.CharField(max_length=20, verbose_name='Общая ширина')
    working_width = models.CharField(max_length=20,
                                     verbose_name='Рабочая ширина')
    length = models.CharField(max_length=20, verbose_name='Длина')
    country = models.CharField(max_length=20,
                               verbose_name='Страна производства')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Terrace(Product):

    class Meta:
        verbose_name = 'Террасная доска'
        verbose_name_plural = 'Террасная доска'

    depth = models.CharField(max_length=20, verbose_name='Толщина')
    width = models.CharField(max_length=20, verbose_name='Общая ширина')
    working_width = models.CharField(max_length=20,
                                     verbose_name='Рабочая ширина')
    length = models.CharField(max_length=20, verbose_name='Длина')
    country = models.CharField(max_length=20,
                               verbose_name='Страна производства')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Stairs(Product):

    class Meta:
        verbose_name = 'Лестничные элементы'
        verbose_name_plural = 'Лестничные элементы'

    depth = models.CharField(max_length=20, verbose_name='Толщина')
    width = models.CharField(max_length=20, verbose_name='Общая ширина')
    length = models.CharField(max_length=20, verbose_name='Длина')
    country = models.CharField(max_length=20,
                               verbose_name='Страна производства')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class DoskaPola(Product):

    class Meta:
        verbose_name = 'Доска пола'
        verbose_name_plural = 'Доска пола'

    depth = models.CharField(max_length=20, verbose_name='Толщина')
    width = models.CharField(max_length=20, verbose_name='Общая ширина')
    working_width = models.CharField(max_length=20,
                                     verbose_name='Рабочая ширина')
    length = models.CharField(max_length=20, verbose_name='Длина')
    country = models.CharField(max_length=20,
                               verbose_name='Страна производства')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Brus(Product):

    class Meta:
        verbose_name = 'Брус'
        verbose_name_plural = 'Брус'

    depth = models.CharField(max_length=20, verbose_name='Толщина')
    width = models.CharField(max_length=20, verbose_name='Ширина')
    length = models.CharField(max_length=20, verbose_name='Длина')
    country = models.CharField(max_length=20,
                               verbose_name='Страна производства')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'

    user = models.ForeignKey('Customer', verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина',
                             on_delete=models.CASCADE,
                             related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name='Стоимость')

    def __str__(self):
        return f'Продукты в корзине {self.content_object.title}'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    owner = models.ForeignKey('Customer', null=True, verbose_name='Покупатель',
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True,
                                      related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, default=0,
                                      decimal_places=2,
                                      verbose_name='Стоимость')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, verbose_name='Номер телефона',
                             null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name='Адрес',
                               null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя',
                                    related_name='related_customer')

    def __str__(self):
        return f'{self.user.first_name}{self.user.last_name}'


class Order(models.Model):

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    BUYING_TYPE_CHOICE = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель',
                                 on_delete=models.CASCADE,
                                 related_name='related_orders')
    first_name = models.CharField(max_length=55, verbose_name='Имя')
    last_name = models.CharField(max_length=55, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона',
                             null=True, blank=True)
    email = models.EmailField(max_length=100, verbose_name='Email', null=True,
                              blank=True)
    cart = models.ForeignKey(Cart, verbose_name='Корзина',
                             on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=300, verbose_name='Адрес доставки',
                               null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус заказа',
                              choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, verbose_name='Тип доставки',
                                   choices=BUYING_TYPE_CHOICE,
                                   default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name='Коментарий', null=AttributeError,
                               blank=True)
    created_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа',
                                  default=timezone.now)

    def __str__(self):
        return str(self.id)
