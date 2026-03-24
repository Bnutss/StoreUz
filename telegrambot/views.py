from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Category, Product, ProductVariant, TelegramUser, Order


def webapp_index(request):
    categories = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('children')
    return render(request, 'webapp/index.html', {'categories': categories})


@require_GET
def api_categories(request):
    cats = list(
        Category.objects.filter(is_active=True).values('id', 'name', 'slug', 'parent_id', 'order')
    )
    return JsonResponse({'categories': cats})


@require_GET
def api_products(request):
    qs = Product.objects.filter(is_active=True).select_related('category')

    category_slug = request.GET.get('category')
    gender = request.GET.get('gender')
    search = request.GET.get('search')

    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if gender:
        qs = qs.filter(gender=gender)
    if search:
        qs = qs.filter(name__icontains=search)

    qs = qs.prefetch_related('images')
    products = []
    for p in qs:
        main_img = None
        for img in p.images.all():
            if img.is_main:
                main_img = img.image.url
                break
        if not main_img:
            first = p.images.all().first()
            if first:
                main_img = first.image.url
        products.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'discount_price': float(p.discount_price) if p.discount_price else None,
            'actual_price': float(p.actual_price),
            'brand': p.brand,
            'gender': p.gender,
            'category': p.category.name if p.category else None,
            'category_slug': p.category.slug if p.category else None,
            'total_stock': p.total_stock,
            'is_featured': p.is_featured,
            'image': main_img,
        })

    return JsonResponse({'products': products})


@require_GET
def api_product_detail(request, product_id):
    try:
        product = Product.objects.select_related('category').prefetch_related(
            'images', 'variants__color', 'variants__size'
        ).get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)

    variants = []
    for v in product.variants.all():
        variants.append({
            'id': v.id,
            'color': {'id': v.color.id, 'name': v.color.name, 'hex': v.color.hex_code} if v.color else None,
            'size': {'id': v.size.id, 'name': v.size.name, 'type': v.size.size_type} if v.size else None,
            'stock': v.stock,
            'available': v.stock > 0,
        })

    images = [{'id': img.id, 'url': img.image.url, 'is_main': img.is_main} for img in product.images.all()]

    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'discount_price': float(product.discount_price) if product.discount_price else None,
        'actual_price': float(product.actual_price),
        'brand': product.brand,
        'gender': product.gender,
        'category': product.category.name if product.category else None,
        'variants': variants,
        'images': images,
    })


@require_GET
def api_user_orders(request):
    telegram_id = request.GET.get('telegram_id')
    if not telegram_id:
        return JsonResponse({'orders': []})
    try:
        user = TelegramUser.objects.get(telegram_id=telegram_id)
    except TelegramUser.DoesNotExist:
        return JsonResponse({'orders': []})

    orders = Order.objects.filter(user=user).prefetch_related('items').order_by('-created_at')[:20]
    result = []
    for o in orders:
        result.append({
            'id': o.pk,
            'status': o.status,
            'delivery_type': o.delivery_type,
            'total_price': float(o.total_price),
            'items_count': o.items.count(),
            'created_at': o.created_at.strftime('%d.%m.%Y %H:%M'),
        })
    return JsonResponse({'orders': result})
