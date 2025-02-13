from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from tbot.tasks import send_news_as_notification
from .models import (LANGUAGE_OPTIONS, AsvpElem, Bdr, BdrElement,
                     Country, Category, Message, MessageDocument,
                     Court, CourtElement, CourtAssignment, AssignmentElem,
                     Debtors, DebtorsElem,
                     Departure, DepartureElem, DocState, InactiveDocument,
                     SavedSearch,
                     Mvs, News,
                     NewsContent, Search, User)


def status_publish(mdl, request, queryset):
    queryset.update(status='publish')


def status_finish(mdl, request, queryset):
    queryset.update(status='finish')


class DepartureElemAdmin(admin.StackedInline):
    model = DepartureElem
    extra = 0


@admin.register(Departure)
class DepartureAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'days', 'subscribe')
    inlines = [DepartureElemAdmin]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'name', 'name_en', 'date_end', 'role',
                    'date_register', 'unsubscribe_news')

    list_filter = ('role', 'blocked', 'language')

    search_fields = ('chat_id', 'username', 'name', 'name_en')

    readonly_fields = ('date_register', 'get_username', 'chat_id', 'subs_id',
                       'language')

    fieldsets = (
        (None, {
            'fields': (
                'chat_id', 'get_username', 'name', 'name_en', 'language',
                'date_end', 'subs_id', 'role', 'blocked', 'date_register',
                'unsubscribe_news')
        }),
    )

    @admin.display(ordering='username', description='username')
    def get_username(self, obj):
        if obj.username:
            return format_html(f'<a target="_blank"'
                               f' href="https://t.me/{obj.username}">'
                               f'@{obj.username}</a>')
        else:
            return '-'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ('slug', 'name', 'name_uk', 'name_en')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ('slug', 'name', 'name_uk', 'name_en', 'country', 'parent')


class MessageDocumentInline(admin.StackedInline):
    model = MessageDocument
    exclude = ('width', 'height')
    readonly_fields = ('image_preview',)

    @admin.display(description=_('Preview'))
    def image_preview(self, obj: MessageDocument):
        if obj is not None and obj.src_image:
            img = obj.src_image
            result = '''
                    <div>
                        <img src="{img}" width="150" height="150" alt="{title}"/>
                        <div>[{width} x {height}] ({size} mb)</div>
                    </div>'''.format(
                img=img.thumbnail['300x300'].url, title=obj.message_id or img.name.split('/')[-1].split('.')[0],
                width=obj.width, height=obj.height, size=round(img.size / 1024 ** 2, 3)
            )
            return mark_safe(result)
        return '-'

    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_filter = ('category', 'user', 'dt_create')
    list_display = ('category', 'user', 'dt_create')
    readonly_fields = ('dt_create', )

    inlines = (MessageDocumentInline,)


class NewsContentInline(admin.TabularInline):
    model = NewsContent
    extra = 0


class NewsForms(forms.ModelForm):
    language = forms.MultipleChoiceField(choices=LANGUAGE_OPTIONS,
                                         label='Локализация',
                                         # widget=forms.CheckboxSelectMultiple()
                                         )

    class Meta:
        model = News
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewsForms, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.initial['language'] = eval(kwargs['instance'].language)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'text', 'get_language', 'status')

    list_filter = ('date', 'status')

    form = NewsForms

    inlines = [NewsContentInline]

    class Media:
        js = ('https://code.jquery.com/jquery-3.6.0.min.js', 'js/news.js')

    @admin.display(ordering='language', description='Локализация')
    def get_language(self, obj):
        return ', '.join(eval(obj.language))

    def get_actions(self, request):
        actions = super().get_actions(request)

        actions.update(
            publish=(
                status_publish, 'publish', 'Публиковать'
            ),
            finish=(
                status_finish, 'finish', 'Завершить'
            )
        )

        return actions

    def save_model(self, request, obj, form, change):
        super(NewsAdmin, self).save_model(request, obj, form, change)
        if obj.status == 'send':
            print('send')
            send_news_as_notification.apply_async(args=[obj.id])


class BdrElemInlines(admin.StackedInline):
    model = BdrElement
    extra = 0


@admin.register(Bdr)
class BdrAdmin(admin.ModelAdmin):
    list_display = ('user', 'plate', 'document', 'date_start', 'count', 'status')

    inlines = [BdrElemInlines]

    @admin.display(description='кол-во штрафов')
    def count(self, obj):
        return obj.bdr_elem.count()


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_name', 'date_start', 'status')

    @admin.display(description='ФИО')
    def get_name(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'


class CourtElemInlines(admin.StackedInline):
    model = CourtElement
    extra = 0


class CourtAssignInlines(admin.StackedInline):
    model = AssignmentElem
    extra = 0


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('number', 'code', 'court', 'claimant',
                    'date', 'count')

    inlines = [CourtElemInlines, CourtAssignInlines]

    @admin.display(description='кол-во решений')
    def count(self, obj):
        return obj.court_elem.count()


@admin.register(CourtAssignment)
class CourtAssignmentAdmin(admin.ModelAdmin):
    list_display = ('search', 'subscribe', 'count')
    inlines = [CourtAssignInlines]

    @admin.display(description='кол-во дел')
    def count(self, obj):
        return obj.assign_elem.count()


@admin.register(Mvs)
class MvsAdmin(admin.ModelAdmin):
    list_display = ('region', 'category', 'disappearance', 'birth',
                    'accusations', 'precaution', 'link')


@admin.register(InactiveDocument)
class InactiveDocumentAdmin(admin.ModelAdmin):
    list_display = ('type_doc', 'series', 'number', 'status')

    readonly_fields = ('status', 'description')


@admin.register(DocState)
class DocStateAdmin(admin.ModelAdmin):
    list_display = ('type_doc', 'series', 'number')

    readonly_fields = ('description',)

class DebtorsElemInline(admin.StackedInline):
    model = DebtorsElem
    extra = 0


@admin.register(Debtors)
class DebtorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'search', 'subscribe')
    inlines = [DebtorsElemInline]


@admin.register(AsvpElem)
class AsvpElemAdmin(admin.ModelAdmin):
    list_display = ('id', 'debtors', 'agency', 'status')


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'state', 'saved_data')
    exclude = ('data_as_str',)