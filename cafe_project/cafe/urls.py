from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signup.html", views.signup, name="signup_html"),

    # Login using custom view
    path("login/", views.login_view, name="login"),
    path("login.html", views.login_view, name="login_html"),

    # Logout using Django's built-in view
    path("logout/", LogoutView.as_view(next_page='home'), name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("menu/", views.menu, name="menu"),
    path("order/", views.order, name="order"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("study/", views.study, name="study"),
    path("products/", views.product_list, name="product_list"),
    path("contact-us/", views.contact_us, name="contactus"),
    path("cart/", views.shopping_cart, name="shoppingcart"),
    path("cart/api/", views.get_cart, name="get_cart"),
    path("cart/api/update/", views.update_cart, name="update_cart"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.profile_update, name="profile_update"),
    path("profile/change-password/", views.change_password, name="change_password"),
    path("profile/upload-image/", views.upload_profile_image, name="upload_profile_image"),
    path("profile/send-verification-code/", views.send_verification_code, name="send_verification_code"),
    path("profile/verify-code/", views.verify_code, name="verify_code"),
    path("index/", views.index, name="index"),
    path("menu/api/", views.menu_api, name="menu_api"),
    path("menu/<int:item_id>/", views.menu_item_api, name="menu_item_api"),
    path("menu/signup.html", views.signup, name="menu_signup_html"),
    path("menu/login.html", views.login_view, name="menu_login_html"),
]
