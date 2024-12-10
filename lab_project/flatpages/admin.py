from django.contrib import admin
from .models import Lesson
from .models import  Book
from .models import DjangoTest
from .models import Course, Cart, CartItem
from .models import Purchase


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Убирает дополнительные пустые строки для элементов

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')  # Отображаем пользователя и дату создания корзины
    inlines = [CartItemInline]  # Включаем CartItem как встроенный элемент на странице корзины
    search_fields = ('user__username',)  # Добавляем возможность поиска по имени пользователя
    list_filter = ('created_at',)  # Добавляем фильтр по дате создания

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'course', 'quantity', 'get_total_price')  # Отображаем корзину, курс и общую цену
    list_filter = ('cart', 'course')  # Фильтры для удобной навигации
    search_fields = ('course__title',)  # Поле поиска по названию курса

admin.site.register(Lesson)
admin.site.register(Book)
admin.site.register(DjangoTest)
admin.site.register(Course)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'purchase_date')
    list_filter = ('course', 'purchase_date')
    search_fields = ('user__username', 'course__title')