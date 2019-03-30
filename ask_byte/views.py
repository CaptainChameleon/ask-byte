from django.utils import timezone
# from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.template import loader

from .view_utils import *
from .models import *


# @cache_page(0)
@cache_page(60 * 60 * 12)
def index(request):
    question_parent_cats = QuestionCategory.objects.filter(parent_category__isnull=True)
    category_tree = generate_html_collapsible_tree(question_parent_cats)
    # category_tree = get_category_tree(question_parent_cats)
    # category_tree = question_parent_cats.values_list()
    template = loader.get_template('ask_byte/index.html')
    context = {'category_tree': category_tree}
    return HttpResponse(template.render(context, request))


@csrf_protect
def question_input(request):
    post_data = request.POST

    if 'question-cat' not in post_data.keys() or 'question-text' not in post_data.keys():
        return JsonResponse({'success': False, 'fishy': True})

    # AttributeError: 'NoneType' object has no attribute 'split'
    question_text = " ".join(post_data['question-text'].split())
    question_cat_id = post_data['question-cat']

    if question_cat_id == "":
        return JsonResponse({'success': False, 'fishy': True})

    if len(question_text) < 4:
        return JsonResponse({'success': False, 'error': '¡Tu consulta es muy corta!'})

    if len(question_text) > 200:
        return JsonResponse({'success': False, 'error': '¡Tu consulta es muy larga!'})

    question_cat = QuestionCategory.objects.filter(pk=int(question_cat_id))

    if not question_cat.exists():
        return JsonResponse({'success': False, 'fishy': True})

    question_cat = question_cat[0]
    question = UserQuestion(category=question_cat, text=question_text, date=timezone.now())
    question.save()
    return JsonResponse({'success': True})
