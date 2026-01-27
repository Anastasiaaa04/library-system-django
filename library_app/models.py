from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    """Модель автора книги"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Genre(models.Model):
    """Модель жанра книги"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ManyToManyField(Genre, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(2100)]
    )
    pages = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='books/pdfs/', null=True, blank=True)
    available_copies = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title

    def get_average_rating(self):
        """Получить средний рейтинг книги"""
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class Reader(models.Model):
    """Модель читателя (профиль пользователя)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reader_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='readers/avatars/', null=True, blank=True)
    membership_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'

    def __str__(self):
        return f"{self.user.username} - {self.user.get_full_name()}"


class BookIssue(models.Model):
    """Модель выдачи книги"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='issues')
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Выдача книги'
        verbose_name_plural = 'Выдачи книг'

    def __str__(self):
        return f"{self.book.title} - {self.reader.user.username}"

    def calculate_fine(self):
        """Расчет штрафа за просрочку"""
        if self.return_date and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            return days_overdue * 10  # 10 рублей за день просрочки
        return 0


class BookReturn(models.Model):
    """Модель возврата книги"""
    issue = models.OneToOneField(BookIssue, on_delete=models.CASCADE, related_name='return_record')
    return_date = models.DateTimeField(auto_now_add=True)
    condition_notes = models.TextField(blank=True)
    is_damaged = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Возврат книги'
        verbose_name_plural = 'Возвраты книг'

    def __str__(self):
        return f"Return: {self.issue.book.title} by {self.issue.reader.user.username}"


class BookReview(models.Model):
    """Модель отзыва о книге"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв о книге'
        verbose_name_plural = 'Отзывы о книгах'

    def __str__(self):
        return f"Review by {self.reader.user.username} for {self.book.title}"