from django.contrib import admin
from .models import Quiz, Choice, Nonce, UserInfo

# Register your models here.


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


class QuizAdmin(admin.ModelAdmin):

    list_display = ('statement', 'choices_str',
                    'is_approved', 'is_public', 'user')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'is_public',)

    fieldsets = (
        (None, {
            "fields": ['title', 'statement', 'thumbnail_image_url', 'is_approved', 'is_public'],
        }),
    )
    inlines = [ChoiceInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Choice)
admin.site.register(Nonce)
admin.site.register(UserInfo)
