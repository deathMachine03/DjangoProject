from django.contrib import admin
from django.urls import path
from flatpages import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('books/', views.books, name='books'),  # Страница с книгами
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),  # URL для отдельной книги
    path('register/', views.register, name='register'),
    path('tests/', views.tests, name='tests'),  # путь для страницы тестов
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('cart/add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),  # Новый URL для очистки корзины
    path('cart/purchase/<int:course_id>/', views.purchase_course, name='purchase_course'),  # URL для покупки
    path('payment-success/', views.payment_success, name='payment_success'),  # Страница успешной оплаты

]
