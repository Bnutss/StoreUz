from django.contrib import admin
from .models import (
    Category, Color, Size, Product, ProductImage,
    ProductVariant, TelegramUser, Cart, CartItem, Order, OrderItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')
    search_fields = ('name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'size_type', 'order')
    list_filter = ('size_type',)
    ordering = ('size_type', 'order')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'order')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('color', 'size', 'stock')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'gender', 'price', 'discount_price', 'total_stock', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'gender', 'category')
    search_fields = ('name', 'brand', 'sku')
    list_editable = ('is_active', 'is_featured')
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'first_name', 'last_name', 'username', 'phone_number', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name', 'phone_number')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'updated_at')
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'status', 'delivery_type', 'total_price', 'created_at')
    list_filter = ('status', 'delivery_type')
    search_fields = ('user__first_name', 'user__telegram_id', 'delivery_address')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
