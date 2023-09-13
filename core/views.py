import logging
import stripe
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseServerError
from django.views import View
from django.views.generic import ListView, TemplateView
from django.db.models import QuerySet
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, 
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from djangoproject.settings import DEBUG
from .models import Product, Category
from .repository import ProductRepository
from .serializers import StripeSessionCreationSerializer
from .services import PaymentService
from djangoproject.settings import ALLOWED_HOSTS, STRIPE_SECRET_KEY


logger = logging.getLogger("debug")


if not DEBUG:
    class BaseView(View):
        def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            try:
                return super().dispatch(request, *args, **kwargs)
            except Exception as e:
                logger.error(e)
                return HttpResponseServerError(e) if DEBUG else HttpResponseServerError()
    

    class BaseAPIView(APIView):
        def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            try:
                return super().dispatch(request, *args, **kwargs)
            except Exception as e:
                logger.error(e)
                return Response({"success": False, "errors": e}, status=HTTP_500_INTERNAL_SERVER_ERROR)

else:
    class BaseView(View):
        ...


    class BaseAPIView(APIView):
        ...
        


class ProductsView(BaseView, ListView):
    model = Product
    template_name = "core/products.html"
    context_object_name = "products"
    category: str

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        self.category = request.path.split("/")[-1]
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        return ProductRepository.get_products_by_category_name_without_time_create_and_time_update(category_name=self.category)


class CategoriesView(BaseView, ListView):
    model = Category
    template_name = "core/categories.html"
    context_object_name = "categories"


class StripeSessionCreationView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        stripe.api_key = STRIPE_SECRET_KEY

        seralizer = StripeSessionCreationSerializer(data=request.GET)
        if seralizer.is_valid():
            if ProductRepository.get_product_by_id(product_id=seralizer.validated_data.get("product_id")) is None:
                return Response({"success": False, "errors": "Product not found"}, status=HTTP_404_NOT_FOUND)

            if not PaymentService.register_product_buying_in_redis(
                product_id=seralizer.validated_data.get("product_id"),
                user_id=request.session.get("_auth_user_id")
            ):
                return Response({"success": False}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            line_item = PaymentService.get_line_item(
                name=seralizer.validated_data.get("name"),
                description=seralizer.validated_data.get("description"),
                price=seralizer.validated_data.get("price")
            )

            success_url = f"http://{ALLOWED_HOSTS[1]}:8000{reverse('success_payment_page')}"
            cancel_url = f"http://{ALLOWED_HOSTS[1]}:8000{reverse('cancel_payment_page')}"

            session = stripe.checkout.Session.create(
                line_items=line_item,
                api_key=stripe.api_key,
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url
            )

            return Response({"success": True, "session": session})

        else:
            return Response({"success": False, "errors": seralizer.errors}, status=HTTP_400_BAD_REQUEST)


class SuccessPaymentView(BaseView, TemplateView):
    template_name = "core/success_payment.html"


class PaymentCancelView(BaseView, TemplateView):
    template_name = "core/cancel_payment.html"
    

class DecrementionProductQuantity(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any):
        user_id = request.session.get("_auth_user_id")

        # product_id has type str or None
        product_id = PaymentService.get_product_buying_in_redis(user_id=user_id)

        if product_id is not None:
            PaymentService.delete_product_buying_in_redis(user_id=user_id)
            ProductRepository.decrement_product_quantity(product_id=int(product_id))
            return Response({"success": True})
                
        else:
            return Response({"success": False, "errors": "Product not found"}, status=HTTP_404_NOT_FOUND)


class RootView(BaseView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse("Root page")


class RootAPIView(BaseAPIView): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        return Response({"success": True})
