from django.shortcuts import render, get_object_or_404
from .models import Lesson
from .models import Book
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .models import DjangoTest
from .models import Course, Cart, CartItem
from .models import CartItem, Purchase
from .models import Course, Review
from .forms import ReviewForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def home(request):
    lessons = Lesson.objects.all()  # Убедитесь, что данные загружаются
    return render(request, 'index.html', {'lessons': lessons})

def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на главную страницу или другую страницу после регистрации
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def tests(request):
    tests = DjangoTest.objects.all()
    return render(request, 'tests/tests.html', {'tests': tests})

def tests(request):
    tests = DjangoTest.objects.all()
    results = []
    score = 0

    if request.method == 'POST':
        for test in tests:
            selected_option = request.POST.get(f'question_{test.id}')
            selected_option = int(selected_option) if selected_option else None
            is_correct = selected_option == test.correct_answer
            if is_correct:
                score += 1

            # Получаем текст правильного ответа
            correct_answer_text = getattr(test, f'option{test.correct_answer}')

            results.append({
                'question': test.question,
                'selected': selected_option,
                'correct': test.correct_answer,
                'is_correct': is_correct,
                'correct_answer_text': correct_answer_text,
                'options': {
                    1: test.option1,
                    2: test.option2,
                    3: test.option3,
                    4: test.option4
                }
            })

        return render(request, 'tests/results.html', {
            'score': score,
            'total': tests.count(),
            'results': results
        })

    return render(request, 'tests/tests.html', {'tests': tests})

def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Проверка, существует ли уже элемент в корзине
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, course=course)
    
    # Увеличиваем количество только если элемент уже существовал
    if not item_created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    
    cart_item.save()
    return redirect('cart_detail')

def clear_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()  # Удаляем все элементы корзины
    return redirect('cart_detail')

def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Здесь мы подсчитываем общую сумму вне шаблона
    total_price = 0
    for item in cart.items.all():
        total_price += item.get_total_price()
    return render(request, 'courses/cart_detail.html', {'cart': cart, 'total_price': total_price})

def purchase_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Удаляем элемент из корзины, если он существует
    cart_item = CartItem.objects.filter(cart=cart, course=course).first()
    if cart_item:
        cart_item.delete()

    # Создаем запись о покупке
    Purchase.objects.create(user=request.user, course=course)

    # Получаем email пользователя
    user_email = request.user.email
    if not user_email:
        # Если у пользователя отсутствует email, показываем сообщение об ошибке
        messages.error(request, "Ваш email не указан. Обновите профиль, чтобы получать уведомления.")
        return redirect('cart_detail')

    # Отправляем уведомление на email
    try:
        send_mail(
            subject=f"Подтверждение покупки курса: {course.title}",
            message=f"Здравствуйте, {request.user.username}!\n\n"
                    f"Вы успешно приобрели курс \"{course.title}\" за {course.price}$.\n"
                    "Спасибо за покупку! Мы рады, что вы выбрали наш сервис.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,  # Показывать ошибки, если email не может быть отправлен
        )
        messages.success(request, "Письмо с подтверждением отправлено на ваш email.")
    except Exception as e:
        # Обрабатываем ошибки отправки email
        messages.error(request, f"Произошла ошибка при отправке письма: {str(e)}")

    # Перенаправляем пользователя
    return redirect('cart_detail')

def payment_success(request):
    return render(request, 'courses/payment_success.html')

