from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta, date
from .models import Book, Author, Genre, Reader, BookIssue, BookReturn, BookReview
from .forms import (
    UserRegisterForm, UserLoginForm, BookSearchForm,
    BookReviewForm, ReaderProfileForm, BookIssueForm
)
from django.core.paginator import Paginator


def home(request):
    """Главная страница сайта"""
    popular_books = Book.objects.annotate(
        review_count=Count('reviews')
    ).order_by('-review_count', '-rating')[:6]

    # Получаем новые книги
    new_books = Book.objects.order_by('-created_at')[:6]

    # Получаем статистику
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_genres = Genre.objects.count()
    total_readers = Reader.objects.count()

    context = {
        'popular_books': popular_books,
        'new_books': new_books,
        'total_books': total_books,
        'total_authors': total_authors,
        'total_genres': total_genres,
        'total_readers': total_readers,
    }
    return render(request, 'library_app/home.html', context)


# Каталог книг
def catalog(request):
    """Каталог книг с поиском и фильтрацией"""
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        if form.cleaned_data['title']:
            books = books.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['author']:
            books = books.filter(
                Q(author__first_name__icontains=form.cleaned_data['author']) |
                Q(author__last_name__icontains=form.cleaned_data['author'])
            )
        if form.cleaned_data['genre']:
            books = books.filter(genre=form.cleaned_data['genre'])
        if form.cleaned_data['min_year']:
            books = books.filter(publication_year__gte=form.cleaned_data['min_year'])
        if form.cleaned_data['max_year']:
            books = books.filter(publication_year__lte=form.cleaned_data['max_year'])
        if form.cleaned_data['min_rating']:
            books = books.filter(rating__gte=form.cleaned_data['min_rating'])

    # Сортировка
    sort_by = request.GET.get('sort_by', 'title')
    if sort_by == 'rating':
        books = books.order_by('-rating')
    elif sort_by == 'year':
        books = books.order_by('-publication_year')
    else:
        books = books.order_by('title')

    # Пагинация
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'sort_by': sort_by,
    }
    return render(request, 'library_app/catalog.html', context)


# Детальная страница книги
def book_detail(request, book_id):
    """Детальная страница книги"""
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    average_rating = book.get_average_rating()

    # Форма отзыва (только для авторизованных)
    review_form = None
    if request.user.is_authenticated:
        if request.method == 'POST' and 'review_submit' in request.POST:
            review_form = BookReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.book = book
                review.reader = request.user.reader_profile
                review.save()
                messages.success(request, 'Отзыв успешно добавлен!')
                return redirect('book_detail', book_id=book_id)
        else:
            review_form = BookReviewForm()

    # Получаем похожие книги
    similar_books = Book.objects.filter(genre__in=book.genre.all()).exclude(id=book_id).distinct()[:4]

    context = {
        'book': book,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'similar_books': similar_books,
    }
    return render(request, 'library_app/book_detail.html', context)


# Регистрация пользователя
def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('catalog')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем профиль читателя
            Reader.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('catalog')
    else:
        form = UserRegisterForm()

    return render(request, 'library_app/register.html', {'form': form})


# Вход в систему
def user_login(request):
    """Вход пользователя в систему"""
    if request.user.is_authenticated:
        return redirect('catalog')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # Обработка "Запомнить меня"
                if form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(1209600)  # 2 недели
                else:
                    request.session.set_expiry(0)  # До закрытия браузера

                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('catalog')
    else:
        form = UserLoginForm()

    return render(request, 'library_app/login.html', {'form': form})


# Выход из системы
@login_required
def user_logout(request):
    """Выход пользователя из системы"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('home')


# Профиль пользователя
@login_required
def profile(request):
    """Профиль пользователя"""
    reader = request.user.reader_profile
    issued_books = BookIssue.objects.filter(reader=reader, is_returned=False)
    reading_history = BookIssue.objects.filter(reader=reader).order_by('-issue_date')[:10]

    if request.method == 'POST':
        form = ReaderProfileForm(request.POST, request.FILES, instance=reader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = ReaderProfileForm(instance=reader)

    context = {
        'reader': reader,
        'issued_books': issued_books,
        'reading_history': reading_history,
        'form': form,
    }
    return render(request, 'library_app/profile.html', context)


# Выдача книги
@login_required
def issue_book(request):
    """Выдача книги читателю"""
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            due_date = form.cleaned_data['due_date']

            # Проверяем доступность книги
            if book.available_copies <= 0:
                messages.error(request, 'Книга недоступна для выдачи.')
                return redirect('issue_book')

            # Создаем запись о выдаче
            BookIssue.objects.create(
                book=book,
                reader=request.user.reader_profile,
                due_date=due_date
            )

            # Уменьшаем количество доступных копий
            book.available_copies -= 1
            book.save()

            messages.success(request, f'Книга "{book.title}" успешно выдана!')
            return redirect('profile')
    else:
        form = BookIssueForm()

    return render(request, 'library_app/issue_book.html', {'form': form})


# Возврат книги
@login_required
def return_book(request, issue_id):
    """Возврат книги"""
    issue = get_object_or_404(BookIssue, id=issue_id, reader=request.user.reader_profile, is_returned=False)

    if request.method == 'POST':
        # Отмечаем книгу как возвращенную
        issue.is_returned = True
        issue.return_date = date.today()
        issue.save()

        # Создаем запись о возврате
        BookReturn.objects.create(
            issue=issue,
            condition_notes=request.POST.get('condition_notes', ''),
            is_damaged=request.POST.get('is_damaged') == 'on'
        )

        # Увеличиваем количество доступных копий
        issue.book.available_copies += 1
        issue.book.save()

        # Расчет штрафа
        fine = issue.calculate_fine()
        if fine > 0:
            issue.fine_amount = fine
            issue.save()
            messages.warning(request, f'Книга возвращена. Штраф за просрочку: {fine} руб.')
        else:
            messages.success(request, 'Книга успешно возвращена!')

        return redirect('profile')

    return render(request, 'library_app/return_book.html', {'issue': issue})


# История чтения
@login_required
def reading_history(request):
    """История чтения пользователя"""
    reader = request.user.reader_profile
    issues = BookIssue.objects.filter(reader=reader).order_by('-issue_date')

    # Пагинация
    paginator = Paginator(issues, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'library_app/reading_history.html', context)


# Статистика и рекомендации
@login_required
def statistics(request):
    """Статистика и рекомендации"""
    reader = request.user.reader_profile

    # Статистика пользователя
    total_issues = BookIssue.objects.filter(reader=reader).count()
    returned_books = BookIssue.objects.filter(reader=reader, is_returned=True).count()
    current_issues = BookIssue.objects.filter(reader=reader, is_returned=False).count()

    # Самые популярные жанры пользователя
    favorite_genres = Genre.objects.filter(
        books__issues__reader=reader
    ).annotate(
        book_count=Count('books__issues')
    ).order_by('-book_count')[:5]

    # Рекомендации на основе жанров
    if favorite_genres:
        recommended_books = Book.objects.filter(
            genre__in=favorite_genres,
            available_copies__gt=0
        ).exclude(
            issues__reader=reader,
            issues__is_returned=False
        ).distinct()[:8]
    else:
        recommended_books = Book.objects.filter(available_copies__gt=0)[:8]

    # Общая статистика библиотеки
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_genres = Genre.objects.count()
    total_readers = Reader.objects.count()

    # Самые популярные книги
    popular_books = Book.objects.annotate(
        issue_count=Count('issues')
    ).order_by('-issue_count')[:10]

    context = {
        'total_issues': total_issues,
        'returned_books': returned_books,
        'current_issues': current_issues,
        'favorite_genres': favorite_genres,
        'recommended_books': recommended_books,
        'total_books': total_books,
        'total_authors': total_authors,
        'total_genres': total_genres,
        'total_readers': total_readers,
        'popular_books': popular_books,
    }
    return render(request, 'library_app/statistics.html', context)


# Напоминания
@login_required
def reminders(request):
    """Напоминания о возврате книг"""
    reader = request.user.reader_profile
    today = date.today()

    # Книги, которые нужно вернуть в ближайшие 3 дня
    upcoming_returns = BookIssue.objects.filter(
        reader=reader,
        is_returned=False,
        due_date__range=[today, today + timedelta(days=3)]
    )

    # Просроченные книги
    overdue_books = BookIssue.objects.filter(
        reader=reader,
        is_returned=False,
        due_date__lt=today
    )

    # Расчет штрафов
    for issue in overdue_books:
        issue.fine_amount = issue.calculate_fine()

    context = {
        'upcoming_returns': upcoming_returns,
        'overdue_books': overdue_books,
    }
    return render(request, 'library_app/reminders.html', context)


# Страница авторов
def authors_list(request):
    """Список авторов"""
    authors = Author.objects.all()

    # Пагинация
    paginator = Paginator(authors, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'library_app/authors_list.html', context)


# Детальная страница автора
def author_detail(request, author_id):
    """Детальная страница автора"""
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()

    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'library_app/author_detail.html', context)


# Страница жанров
def genres_list(request):
    """Список жанров"""
    genres = Genre.objects.all()

    context = {
        'genres': genres,
    }
    return render(request, 'library_app/genres_list.html', context)