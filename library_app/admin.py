from django.contrib import admin
from django.utils.html import format_html
from .models import Author, Genre, Book, Reader, BookIssue, BookReturn, BookReview


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'birth_date', 'photo_preview']
    list_filter = ['birth_date']
    search_fields = ['last_name', 'first_name']

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; border-radius: 50%; object-fit: cover;"/>',
                obj.photo.url
            )
        return "—"

    photo_preview.short_description = 'Фото'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'cover_preview', 'available_copies', 'rating']
    list_filter = ['genre', 'publication_year', 'available_copies']
    search_fields = ['title', 'author__last_name', 'isbn']
    filter_horizontal = ['genre']

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 75px; border-radius: 3px;"/>',
                obj.cover_image.url
            )
        return "—"

    cover_preview.short_description = 'Обложка'


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'membership_date', 'avatar_preview', 'is_active']
    list_filter = ['is_active', 'membership_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-width: 40px; max-height: 40px; border-radius: 50%; object-fit: cover;"/>',
                obj.avatar.url
            )
        return "—"

    avatar_preview.short_description = 'Аватар'


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'reader', 'issue_date', 'due_date', 'return_date', 'is_returned', 'fine_amount']
    list_filter = ['is_returned', 'issue_date', 'due_date']
    search_fields = ['book__title', 'reader__user__username']
    date_hierarchy = 'issue_date'
    readonly_fields = ['fine_amount']


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