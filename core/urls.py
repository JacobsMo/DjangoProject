from django.urls import path
from .views import (
    ProductsView, CategoriesView, StripeSessionCreationView,
    RootView, SuccessPaymentView, PaymentCancelView, DecrementionProductQuantity, 
    RootAPIView
)
from djangoproject.settings import BASE_API_URL


urlpatterns = [
    path("products/<slug:category>", ProductsView.as_view(), name="products_page"),
    path("categories/", CategoriesView.as_view(), name="categories_page"),
    path(f"{BASE_API_URL}/stripe/session/", StripeSessionCreationView.as_view(), name="stripe_session_creation_api"),
    path("payment/success/", SuccessPaymentView.as_view(), name="success_payment_page"),
    path("", RootView.as_view(), name="root_page"),
    path("payment/cancel/", PaymentCancelView.as_view(), name="cancel_payment_page"),
    path(f"{BASE_API_URL}/payment/decrement_product_quantity/", DecrementionProductQuantity.as_view(), name="decrement_product_quantity_api"),
    path(f"{BASE_API_URL}/", RootAPIView.as_view(), name="root_api"),
]
