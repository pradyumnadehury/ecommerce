from django.urls import path
from . import views

urlpatterns=[
    path("",views.ProductListView.as_view(),name="product_list"),
    path("product/<slug:slug>/",views.ProductDetailView.as_view(),name="product_detail"),
    #The name of the URLConf keyword argument that contains the slug. By default, slug_url_kwarg is 'slug'.
    #-------------------------------------------------------------------------------------------
    path("cart/",views.CartDetailView.as_view(),name="cart_detail"),
    path("cart/add/<int:product_id>/",views.CartAddView.as_view(),name="cart_add"),
    path("cart/update/<int:product_id>/",views.CartUpdateView.as_view(),name="cart_update"),
    path("cart/remove/<int:product_id>",views.CartRemoveView.as_view(),name="cart_remove"),
    #--------------------------------------------------------------------------------------------
    path("checkout/",views.Checkoutview.as_view(),name="checkout"),
    path("orders/",views.OrderListView.as_view(),name="order_list"),
    path("orders/<int:pk>/",views.OrderDetailView.as_view(),name="order_detail"),
    #--------------------------------------------------------------------------------------
    path("reports/staff/",views.StaffOrderReportView.as_view(),name="staff_report"),

    #--------------------------------------------------------------------------------------
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),


]