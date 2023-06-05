from django.urls import path

from .views import home, register, log_in, admin, customer_home, products_list, product_detail, add_item, update, remove_item, full_remove, cart_detail, place_order, delete, order_page, orders_by_product, log_out


app_name = 'website'

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('log-in/', log_in, name='log_in'),
    path('admin-page/', admin, name='admin'),
    path('customer-home/', customer_home, name='customer_home'),
    path('all-products/', products_list, name='products_list'),
    path('product-detail/<int:product_id>/', product_detail, name='product_detail'),
    path('add-item/<int:product_id>/', add_item, name='add_item'),
    path('update-product/<int:product_id>/', update, name='update'),
    path('order-page/', order_page, name='order_page'),
    path('orders-by-product/<int:product_id>/', orders_by_product, name='orders_by_product'),
    path('remove-item/<int:product_id>/', remove_item, name='remove_item'),
    path('full-remove/<int:product_id>/', full_remove, name='full_remove'),
    path('cart-detail/', cart_detail, name='cart_detail'),
    path('place-order/<str:total>/', place_order, name='place_order'),

    path('delete/<int:product_id>/', delete, name='delete'),
    path('log-out/', log_out, name='log_out'),
]
