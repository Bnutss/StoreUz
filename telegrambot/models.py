from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        if self.parent:
            return f'{self.parent.name} / {self.name}'
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    hex_code = models.CharField(max_length=7, verbose_name='HEX код', help_text='Например: #FF5733')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['name']

    def __str__(self):
        return self.name


class Size(models.Model):
    SIZE_TYPE_CHOICES = [
        ('clothing', 'Одежда'),
        ('shoes', 'Обувь'),
        ('universal', 'Универсальный'),
    ]

    name = models.CharField(max_length=20, verbose_name='Размер')
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE_CHOICES, default='clothing', verbose_name='Тип размера')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['size_type', 'order', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_size_type_display()})'


class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Мужской'),
        ('women', 'Женский'),
        ('children', 'Детский'),
        ('unisex', 'Унисекс'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name='Категория')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex', verbose_name='Пол')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена (сум)')
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Цена со скидкой (сум)')
    brand = models.CharField(max_length=255, blank=True, verbose_name='Бренд')
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='Артикул')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемый')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def actual_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def total_stock(self):
        return self.variants.aggregate(total=models.Sum('stock'))['total'] or 0

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Главное фото')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['-is_main', 'order']

    def __str__(self):
        return f'Фото {self.product.name}'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='Товар')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Цвет')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Размер')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')

    class Meta:
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товаров'
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        parts = [self.product.name]
        if self.color:
            parts.append(self.color.name)
        if self.size:
            parts.append(self.size.name)
        return ' / '.join(parts)

    @property
    def is_available(self):
        return self.stock > 0


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Username')
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'

    def __str__(self):
        return f'{self.first_name} ({self.telegram_id})'


class Cart(models.Model):
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {self.user}'

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name='Вариант товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'
        unique_together = ('cart', 'variant')

    def __str__(self):
        return f'{self.variant} x{self.quantity}'

    @property
    def total_price(self):
        if not self.variant or not self.variant.product:
            return 0
        price = self.variant.product.actual_price
        return (price or 0) * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('delivery', 'Доставка'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта при получении'),
        ('payme', 'PayMe'),
        ('click', 'Click'),
    ]

    user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, related_name='orders', verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='delivery', verbose_name='Тип доставки')
    delivery_address = models.TextField(blank=True, verbose_name='Адрес доставки')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash', verbose_name='Способ оплаты')
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name='Контактный телефон')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Итоговая сумма')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.pk} — {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, verbose_name='Вариант товара')
    product_name = models.CharField(max_length=255, verbose_name='Название товара')
    color_name = models.CharField(max_length=100, blank=True, verbose_name='Цвет')
    size_name = models.CharField(max_length=20, blank=True, verbose_name='Размер')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'

    @property
    def total_price(self):
        return (self.price or 0) * self.quantity
