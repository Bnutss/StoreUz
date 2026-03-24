import random
from django.core.management.base import BaseCommand
from telegrambot.models import (
    Category, Color, Size, Product, ProductImage,
    ProductVariant, TelegramUser, Cart, CartItem, Order, OrderItem
)


CATEGORIES_DATA = [
    {'name': 'Мужская', 'slug': 'men', 'parent': None, 'order': 1},
    {'name': 'Женская', 'slug': 'women', 'parent': None, 'order': 2},
    {'name': 'Детская', 'slug': 'children', 'parent': None, 'order': 3},
    {'name': 'Аксессуары', 'slug': 'accessories', 'parent': None, 'order': 4},
    {'name': 'Одежда', 'slug': 'men-clothing', 'parent': 'men', 'order': 1},
    {'name': 'Обувь', 'slug': 'men-shoes', 'parent': 'men', 'order': 2},
    {'name': 'Спортивная одежда', 'slug': 'men-sport', 'parent': 'men', 'order': 3},
    {'name': 'Одежда', 'slug': 'women-clothing', 'parent': 'women', 'order': 1},
    {'name': 'Обувь', 'slug': 'women-shoes', 'parent': 'women', 'order': 2},
    {'name': 'Платья', 'slug': 'women-dresses', 'parent': 'women', 'order': 3},
    {'name': 'Одежда', 'slug': 'children-clothing', 'parent': 'children', 'order': 1},
    {'name': 'Обувь', 'slug': 'children-shoes', 'parent': 'children', 'order': 2},
    {'name': 'Сумки', 'slug': 'bags', 'parent': 'accessories', 'order': 1},
    {'name': 'Ремни', 'slug': 'belts', 'parent': 'accessories', 'order': 2},
    {'name': 'Головные уборы', 'slug': 'hats', 'parent': 'accessories', 'order': 3},
    {'name': 'Очки', 'slug': 'glasses', 'parent': 'accessories', 'order': 4},
]

COLORS_DATA = [
    {'name': 'Чёрный', 'hex_code': '#000000'},
    {'name': 'Белый', 'hex_code': '#FFFFFF'},
    {'name': 'Красный', 'hex_code': '#E53935'},
    {'name': 'Синий', 'hex_code': '#1E88E5'},
    {'name': 'Тёмно-синий', 'hex_code': '#1A237E'},
    {'name': 'Серый', 'hex_code': '#757575'},
    {'name': 'Бежевый', 'hex_code': '#F5F0E8'},
    {'name': 'Коричневый', 'hex_code': '#6D4C41'},
    {'name': 'Хаки', 'hex_code': '#827717'},
    {'name': 'Розовый', 'hex_code': '#F48FB1'},
    {'name': 'Мятный', 'hex_code': '#80CBC4'},
    {'name': 'Бордовый', 'hex_code': '#880E4F'},
]

SIZES_CLOTHING = ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']
SIZES_SHOES = ['36', '37', '38', '39', '40', '41', '42', '43', '44', '45']
SIZES_KIDS = ['86', '92', '98', '104', '110', '116', '122', '128', '134', '140']
SIZES_UNIVERSAL = ['Без размера']

PRODUCTS_DATA = [
    {
        'name': 'Футболка базовая Oversize',
        'description': 'Классическая оверсайз футболка из 100% хлопка. Мягкая, дышащая, идеально подходит для повседневной носки.',
        'category_slug': 'men-clothing',
        'gender': 'men',
        'price': 89000,
        'discount_price': 69000,
        'brand': 'BasicWear',
        'sku': 'BW-TSHIRT-001',
        'size_type': 'clothing',
        'colors': ['Чёрный', 'Белый', 'Серый', 'Тёмно-синий'],
    },
    {
        'name': 'Джинсы Slim Fit мужские',
        'description': 'Мужские джинсы зауженного кроя из стрейч-денима. Комфортная посадка, не стесняет движений.',
        'category_slug': 'men-clothing',
        'gender': 'men',
        'price': 249000,
        'discount_price': None,
        'brand': 'DenimCo',
        'sku': 'DC-JEANS-M001',
        'size_type': 'clothing',
        'colors': ['Тёмно-синий', 'Чёрный', 'Серый'],
    },
    {
        'name': 'Худи с капюшоном мужское',
        'description': 'Тёплое худи из флиса. Удобный карман-кенгуру, регулируемый капюшон.',
        'category_slug': 'men-sport',
        'gender': 'men',
        'price': 195000,
        'discount_price': 175000,
        'brand': 'SportLife',
        'sku': 'SL-HOODIE-M001',
        'size_type': 'clothing',
        'colors': ['Чёрный', 'Серый', 'Хаки', 'Тёмно-синий'],
    },
    {
        'name': 'Кроссовки мужские Runner Pro',
        'description': 'Лёгкие беговые кроссовки с амортизирующей подошвой. Дышащий верх из сетки.',
        'category_slug': 'men-shoes',
        'gender': 'men',
        'price': 450000,
        'discount_price': 390000,
        'brand': 'RunnerPro',
        'sku': 'RP-SHOES-M001',
        'size_type': 'shoes',
        'colors': ['Чёрный', 'Белый', 'Серый'],
    },
    {
        'name': 'Платье летнее льняное',
        'description': 'Лёгкое женское платье из натурального льна. Свободный крой, идеально для лета.',
        'category_slug': 'women-dresses',
        'gender': 'women',
        'price': 280000,
        'discount_price': 240000,
        'brand': 'EleganceUz',
        'sku': 'EU-DRESS-W001',
        'size_type': 'clothing',
        'colors': ['Бежевый', 'Белый', 'Мятный', 'Розовый'],
    },
    {
        'name': 'Блуза шёлковая женская',
        'description': 'Элегантная блуза из искусственного шёлка. Подходит как для офиса, так и для вечернего выхода.',
        'category_slug': 'women-clothing',
        'gender': 'women',
        'price': 195000,
        'discount_price': None,
        'brand': 'EleganceUz',
        'sku': 'EU-BLOUSE-W001',
        'size_type': 'clothing',
        'colors': ['Белый', 'Чёрный', 'Бордовый', 'Розовый'],
    },
    {
        'name': 'Кроссовки женские Fashion Run',
        'description': 'Стильные женские кроссовки на платформе. Сочетают комфорт и модный дизайн.',
        'category_slug': 'women-shoes',
        'gender': 'women',
        'price': 395000,
        'discount_price': 350000,
        'brand': 'FashionStep',
        'sku': 'FS-SHOES-W001',
        'size_type': 'shoes',
        'colors': ['Белый', 'Чёрный', 'Бежевый'],
    },
    {
        'name': 'Костюм спортивный детский',
        'description': 'Удобный детский спортивный костюм из мягкого трикотажа. Эластичный пояс, карманы.',
        'category_slug': 'children-clothing',
        'gender': 'children',
        'price': 145000,
        'discount_price': 125000,
        'brand': 'KidsWorld',
        'sku': 'KW-SUIT-K001',
        'size_type': 'clothing',
        'colors': ['Синий', 'Красный', 'Серый', 'Розовый'],
    },
    {
        'name': 'Сумка кожаная женская Tote',
        'description': 'Вместительная женская сумка-шопер из натуральной кожи. Надёжная фурнитура, несколько отделений.',
        'category_slug': 'bags',
        'gender': 'women',
        'price': 650000,
        'discount_price': None,
        'brand': 'LeatherLux',
        'sku': 'LL-BAG-W001',
        'size_type': 'universal',
        'colors': ['Чёрный', 'Коричневый', 'Бежевый'],
    },
    {
        'name': 'Ремень кожаный мужской классический',
        'description': 'Мужской кожаный ремень с матовой пряжкой. Ширина 3.5 см, доступны размеры 100–125 см.',
        'category_slug': 'belts',
        'gender': 'men',
        'price': 120000,
        'discount_price': 99000,
        'brand': 'LeatherLux',
        'sku': 'LL-BELT-M001',
        'size_type': 'universal',
        'colors': ['Чёрный', 'Коричневый'],
    },
    {
        'name': 'Кепка унисекс Street',
        'description': 'Стильная кепка с вышитым логотипом. Регулируемый ремешок, подходит на большинство размеров.',
        'category_slug': 'hats',
        'gender': 'unisex',
        'price': 75000,
        'discount_price': None,
        'brand': 'StreetStyle',
        'sku': 'SS-CAP-U001',
        'size_type': 'universal',
        'colors': ['Чёрный', 'Белый', 'Хаки', 'Тёмно-синий'],
    },
    {
        'name': 'Солнцезащитные очки Aviator',
        'description': 'Классические очки-авиаторы с UV400 защитой. Металлическая оправа, поляризованные линзы.',
        'category_slug': 'glasses',
        'gender': 'unisex',
        'price': 180000,
        'discount_price': 150000,
        'brand': 'SunVision',
        'sku': 'SV-GLASSES-U001',
        'size_type': 'universal',
        'colors': ['Чёрный', 'Коричневый', 'Серый'],
    },
]

TELEGRAM_USERS_DATA = [
    {'telegram_id': 100000001, 'username': 'alisher_tashkent', 'first_name': 'Алишер', 'last_name': 'Юсупов', 'phone_number': '+998901234567'},
    {'telegram_id': 100000002, 'username': 'malika_uz', 'first_name': 'Малика', 'last_name': 'Рахимова', 'phone_number': '+998907654321'},
    {'telegram_id': 100000003, 'username': 'bobur99', 'first_name': 'Бобур', 'last_name': 'Каримов', 'phone_number': '+998991112233'},
    {'telegram_id': 100000004, 'username': 'zulfiya_shop', 'first_name': 'Зулфия', 'last_name': 'Азимова', 'phone_number': '+998935556677'},
    {'telegram_id': 100000005, 'username': 'sardor_fit', 'first_name': 'Сардор', 'last_name': 'Мирзаев', 'phone_number': '+998901239876'},
    {'telegram_id': 100000006, 'username': 'dilnoza_fashion', 'first_name': 'Дилноза', 'last_name': 'Хасанова', 'phone_number': '+998712223344'},
    {'telegram_id': 100000007, 'username': 'jamshid_bek', 'first_name': 'Жамшид', 'last_name': 'Бекмуродов', 'phone_number': '+998977778899'},
    {'telegram_id': 100000008, 'username': 'nilufar_style', 'first_name': 'Нилуфар', 'last_name': 'Тошматова', 'phone_number': '+998908889900'},
    {'telegram_id': 100000009, 'username': 'sherzod_tdk', 'first_name': 'Шерзод', 'last_name': 'Норматов', 'phone_number': '+998903334455'},
    {'telegram_id': 100000010, 'username': 'kamola_uz', 'first_name': 'Камола', 'last_name': 'Умарова', 'phone_number': '+998914445566'},
]


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными для магазина'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Начинаем заполнение базы данных...'))

        colors = self._create_colors()
        sizes = self._create_sizes()
        categories = self._create_categories()
        products = self._create_products(categories, colors, sizes)
        users = self._create_telegram_users()
        self._create_orders(users, products)

        self.stdout.write(self.style.SUCCESS('\nБаза данных успешно заполнена!'))
        self.stdout.write(f'  Категорий:  {Category.objects.count()}')
        self.stdout.write(f'  Цветов:     {Color.objects.count()}')
        self.stdout.write(f'  Размеров:   {Size.objects.count()}')
        self.stdout.write(f'  Товаров:    {Product.objects.count()}')
        self.stdout.write(f'  Вариантов:  {ProductVariant.objects.count()}')
        self.stdout.write(f'  Юзеров:     {TelegramUser.objects.count()}')
        self.stdout.write(f'  Заказов:    {Order.objects.count()}')

    def _create_colors(self):
        self.stdout.write('  Создаём цвета...')
        colors = {}
        for data in COLORS_DATA:
            color, _ = Color.objects.get_or_create(name=data['name'], defaults={'hex_code': data['hex_code']})
            colors[color.name] = color
        return colors

    def _create_sizes(self):
        self.stdout.write('  Создаём размеры...')
        sizes = {'clothing': {}, 'shoes': {}, 'universal': {}}

        for i, name in enumerate(SIZES_CLOTHING):
            size, _ = Size.objects.get_or_create(name=name, size_type='clothing', defaults={'order': i})
            sizes['clothing'][name] = size

        for i, name in enumerate(SIZES_SHOES):
            size, _ = Size.objects.get_or_create(name=name, size_type='shoes', defaults={'order': i})
            sizes['shoes'][name] = size

        for i, name in enumerate(SIZES_KIDS):
            size, _ = Size.objects.get_or_create(name=name, size_type='clothing', defaults={'order': i + 20})
            sizes['clothing'][name] = size

        size, _ = Size.objects.get_or_create(name='Без размера', size_type='universal', defaults={'order': 0})
        sizes['universal']['Без размера'] = size

        return sizes

    def _create_categories(self):
        self.stdout.write('  Создаём категории...')
        categories = {}

        for data in CATEGORIES_DATA:
            if data['parent'] is None:
                cat, _ = Category.objects.get_or_create(
                    slug=data['slug'],
                    defaults={'name': data['name'], 'order': data['order']}
                )
                categories[data['slug']] = cat

        for data in CATEGORIES_DATA:
            if data['parent'] is not None:
                parent = categories.get(data['parent'])
                cat, _ = Category.objects.get_or_create(
                    slug=data['slug'],
                    defaults={'name': data['name'], 'parent': parent, 'order': data['order']}
                )
                categories[data['slug']] = cat

        return categories

    def _create_products(self, categories, colors, sizes):
        self.stdout.write('  Создаём товары и варианты...')
        products = []

        for data in PRODUCTS_DATA:
            category = categories.get(data['category_slug'])
            product, created = Product.objects.get_or_create(
                sku=data['sku'],
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'category': category,
                    'gender': data['gender'],
                    'price': data['price'],
                    'discount_price': data['discount_price'],
                    'brand': data['brand'],
                    'is_active': True,
                    'is_featured': random.choice([True, False]),
                }
            )

            if created:
                size_type = data['size_type']
                if size_type == 'clothing':
                    size_pool = list(sizes['clothing'].values())[:7]
                elif size_type == 'shoes':
                    size_pool = list(sizes['shoes'].values())
                else:
                    size_pool = [sizes['universal']['Без размера']]

                for color_name in data['colors']:
                    color = colors.get(color_name)
                    if not color:
                        continue
                    for size in size_pool:
                        stock = random.randint(2, 25)
                        ProductVariant.objects.get_or_create(
                            product=product,
                            color=color,
                            size=size,
                            defaults={'stock': stock}
                        )

            products.append(product)

        return products

    def _create_telegram_users(self):
        self.stdout.write('  Создаём пользователей Telegram...')
        users = []
        for data in TELEGRAM_USERS_DATA:
            user, _ = TelegramUser.objects.get_or_create(
                telegram_id=data['telegram_id'],
                defaults={
                    'username': data['username'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'phone_number': data['phone_number'],
                }
            )
            users.append(user)
        return users

    def _create_orders(self, users, products):
        self.stdout.write('  Создаём заказы...')
        statuses = ['new', 'confirmed', 'paid', 'shipped', 'delivered', 'cancelled']
        delivery_types = ['pickup', 'delivery']
        addresses = [
            'Ташкент, Юнусабадский район, ул. Амира Темура 15',
            'Ташкент, Мирабадский район, ул. Навои 8',
            'Самарканд, ул. Регистан 3',
            'Бухара, Старый город, ул. Ляби-Хауз 12',
            'Ташкент, Чиланзарский район, кв. 10, д. 5',
            'Ташкент, Яккасарайский район, ул. Шота Руставели 22',
            'Фергана, ул. Мустакиллик 7',
            'Андижан, ул. Бобур 19',
            'Наманган, Асакинский район, д. 33',
            'Ташкент, Учтепинский район, ул. Катартал 45',
        ]

        for i, user in enumerate(users):
            if Order.objects.filter(user=user).exists():
                continue

            variants = list(ProductVariant.objects.filter(stock__gt=0).order_by('?')[:random.randint(1, 4)])
            if not variants:
                continue

            total = sum(v.product.actual_price * random.randint(1, 2) for v in variants)
            delivery = random.choice(delivery_types)
            order = Order.objects.create(
                user=user,
                status=statuses[i % len(statuses)],
                delivery_type=delivery,
                delivery_address=addresses[i] if delivery == 'delivery' else '',
                total_price=total,
                comment='',
            )

            for variant in variants:
                qty = random.randint(1, 2)
                OrderItem.objects.create(
                    order=order,
                    variant=variant,
                    product_name=variant.product.name,
                    color_name=variant.color.name if variant.color else '',
                    size_name=variant.size.name if variant.size else '',
                    price=variant.product.actual_price,
                    quantity=qty,
                )
