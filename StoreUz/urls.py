from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from telegrambot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webapp/', views.webapp_index, name='webapp'),
    path('api/categories/', views.api_categories, name='api-categories'),
    path('api/products/', views.api_products, name='api-products'),
    path('api/products/<int:product_id>/', views.api_product_detail, name='api-product-detail'),
    path('api/user-orders/', views.api_user_orders, name='api-user-orders'),
    path('api/orders/create/', views.api_create_order, name='api-create-order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
