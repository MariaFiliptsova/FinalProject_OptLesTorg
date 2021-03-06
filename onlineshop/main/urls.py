from django.urls import path
from .views import (
    BaseView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQuantityView,
    CheckOutView,
    MakeOrderView,
    About,
    Contact,
    ThankYou,
)

urlpatterns = [
    path('', BaseView.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('make-order/thank_you/', ThankYou.as_view(), name='thank_you'),
    path('category/<str:slug>/', CategoryDetailView.as_view(),
         name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(),
         name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/',
         DeleteFromCartView.as_view(),
         name='delete_from_cart'),
    path('change-quantity/<str:ct_model>/<str:slug>/',
         ChangeQuantityView.as_view(),
         name='change_quantity'),
    path('check-out/', CheckOutView.as_view(), name='check_out'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),

]