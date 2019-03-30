from django.http import HttpResponse
from django.urls import path
from django.contrib import admin

from .file_utils import *
from .models import *

import os


class CustomAdminSite(admin.AdminSite):
    site_header = 'Byte administration'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download-dataset', self.admin_view(self.generate_dataset), name='download-dataset')
        ]
        return custom_urls + urls

    def generate_dataset(self, request):
        categories = QuestionCategory.objects.all().values()
        user_questions = UserQuestion.objects.all().values()

        categories_csv = generate_temp_csv_from_queryset_values(categories)
        user_questions_csv = generate_temp_csv_from_queryset_values(user_questions)

        dataset = generate_temp_zipfile(['categories.csv', 'user_questions.csv'],
                                        [categories_csv.read(), user_questions_csv.read()])

        response = HttpResponse(dataset.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="ask_byte_data.zip"'
        response['Content-Length'] = dataset.tell()

        return response


# @admin.register(QuestionCategory)
class AdminQuestionCat (admin.ModelAdmin):

    list_display = ('name', 'parent_category')
    search_fields = ['name']


# @admin.register(UserQuestion)
class AdminUserQuestion (admin.ModelAdmin):

    list_display = ('text', 'category', 'date')
    date_hierarchy = 'date'
    search_fields = ['category']


admin.site = CustomAdminSite()

admin.site.register(QuestionCategory, AdminQuestionCat)
admin.site.register(UserQuestion, AdminUserQuestion)


