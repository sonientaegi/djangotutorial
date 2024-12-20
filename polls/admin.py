from django.contrib import admin
from django.db.models import Count

# Register your models here.
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class NumOfChoicesFilter(admin.SimpleListFilter):
    title = "Number of Choices"
    parameter_name = "choice_count"
    def lookups(self, request, model_admin):
        return (
            ('0', '0'),
            ('2', '~2'),
            ('3', '3~'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == '0':
            return queryset.filter(choice_count=0)
        elif value == '2':
            return queryset.filter(choice_count__gte=1).filter(choice_count__lte=2)
        elif value == '3':
            return queryset.filter(choice_count__gte=3)
        else:
            return queryset

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date infsormation', {'fields': ['pub_date'], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', "num_of_choices", "was_published_recently")
    list_filter = ['pub_date', NumOfChoicesFilter]
    search_fields = ['question_text']

    # get_queryset을 override 하면서, annotate를 추가한다.
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(choice_count=Count('choice'))

admin.site.register(Question, QuestionAdmin)