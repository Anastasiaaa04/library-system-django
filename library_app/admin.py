from django.contrib import admin
from .models import Author, Genre, Book, Reader, BookIssue, BookReturn, BookReview
from django.utils.html import format_html


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'birth_date', 'photo_preview']
    list_filter = ['birth_date']
    search_fields = ['last_name', 'first_name']
    readonly_fields = ['photo_preview']

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.photo.url)
        return "Нет фото"

    photo_preview.short_description = 'Превью'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'available_copies', 'rating', 'cover_preview']
    list_filter = ['genre', 'publication_year', 'available_copies']
    search_fields = ['title', 'author__last_name', 'isbn']
    readonly_fields = ['cover_preview']

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="70" style="object-fit: cover;"/>', obj.cover_image.url)
        return "Нет обложки"

    cover_preview.short_description = 'Обложка'


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'membership_date', 'avatar_preview', 'is_active']
    list_filter = ['is_active', 'membership_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['avatar_preview']

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;"/>',
                               obj.avatar.url)
        return "Нет аватара"

    avatar_preview.short_description = 'Аватар'


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'reader', 'issue_date', 'due_date', 'return_date', 'is_returned', 'fine_amount']
    list_filter = ['is_returned', 'issue_date', 'due_date']
    search_fields = ['book__title', 'reader__user__username']
    date_hierarchy = 'issue_date'


@admin.register(BookReturn)
class BookReturnAdmin(admin.ModelAdmin):
    list_display = ['issue', 'return_date', 'is_damaged']
    list_filter = ['is_damaged', 'return_date']
    search_fields = ['issue__book__title', 'issue__reader__user__username']


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'reader', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'reader__user__username']