from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Inicio
    path("", views.index, name="index"),
    # Login & Sign-up
    path('signup', views.registro_view, name='signup'),
    path('login', views.login_view, name='login'),
    

    path("carrito", views.carrito, name="carrito"),
    path("convertir", views.convertir_divisa, name="convertir"),
    path("reconvertir", views.reconvertir_divisa, name="reconvertir"),

    # PRODUCTO
    path("create_prod", views.productoAdd, name="create_prod"),
    path('read_prod/<str:pk>', views.productoRead, name='read_prod'),
    path('update_prod', views.productoUpdate, name='update_prod'),
    path('delete_prod/<str:pk>', views.productoDel, name='delete_prod'),
    path('list_prod', views.productoList, name='list_prod'),

    # STOCK
    path("create_stock", views.stockAdd, name="create_stock"),
    path('read_stock/<str:pk>', views.stockRead, name='read_stock'),
    path('update_stock', views.stockUpdate, name='update_stock'),
    path('delete_stock/<str:pk>', views.stockDel, name='delete_stock'),
    path('list_stock', views.stockList, name='list_stock'),

    # TRANSBANK
    path('webpay/plus/amount-form/', views.webpay_plus_amount_form, name='webpay_plus_amount_form'),
    #path('webpay/plus/create/', views.webpay_plus_create, name='webpay_plus_create'),
    path('webpay/plus/commit/', views.webpay_plus_create, name='webpay_plus_commit'),
    path('webpay/plus/commit-error/', views.webpay_plus_commit_error, name='webpay_plus_commit_error'),
    path('webpay/plus/refund/', views.webpay_plus_refund, name='webpay_plus_refund'),
    path('webpay/plus/refund-form/', views.webpay_plus_refund_form, name='webpay_plus_refund_form'),
    path('webpay/plus/status-form/', views.status_form, name='status_form'),
    path('webpay/plus/status/', views.status, name='status'),

    # CARRITO
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

