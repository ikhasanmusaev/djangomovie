from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'url')
    list_display_links = ('name',)
    readonly_fields = ('id',)


class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('email', 'name')


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height=100px width=auto>')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_display_links = ('title', 'url')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    readonly_fields = ('id', 'get_image')
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    list_editable = ('draft',)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("category", "url", "draft",),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} height=100px width=auto>')
    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    list_display_links = ('name',)
    readonly_fields = ('id',)


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ('name', 'url')
    list_display_links = ('url', )


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    list_display = ('name', 'age', 'get_image')
    list_display_links = ('age', )
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height=50px width=auto>')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie', 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height=50px width=auto>')

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar),

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
