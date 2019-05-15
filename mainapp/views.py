import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
# from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, PostPhoto, Tag, Category, Document, Article, Message, Contact
from .models import Registry, Menu
from .models import Staff
from .forms import PostForm, ArticleForm, DocumentForm
from .forms import SendMessageForm, SubscribeForm, AskQuestionForm, SearchRegistryForm
from .adapters import MessageModelAdapter
from .message_tracker import MessageTracker
from .utilites import UrlMaker
from .registry_import import Importer, data_url

# Create your views here.

def index(request):
    #TODO:  сделать когда-нибудь вывод форм на глваную
    title = 'Головной аттестационный центр Восточно-Сибирского региона'
    """this is mainpage view with forms handler and adapter to messages"""
    # tracker = MessageTracker()
    if request.method == 'POST':
        request_to_dict = dict(zip(request.POST.keys(), request.POST.values()))
        form_select = {
            'send_message_button': SendMessageForm,
            'subscribe_button': SubscribeForm,
            'ask_question': AskQuestionForm,
        }
        for key in form_select.keys():
            if key in request_to_dict:
                print('got you!', key)
                form_class = form_select[key]
        form = form_class(request_to_dict)
        if form.is_valid():

            # saving form data to messages (need to be cleaned in future)
            adapted_data = MessageModelAdapter(request_to_dict)
            adapted_data.save_to_message()
            print('adapted data saved to database')
            tracker.check_messages()
            tracker.notify_observers()
        else:
            raise ValidationError('form not valid')

    # docs = Document.objects.filter(
    #     publish_on_main_page=True).order_by('-created_date')[:3]

    # main_page_news = Post.objects.filter(
    #     publish_on_main_page=True).order_by('-published_date')[:7]

    #Посты с картинками
    # posts = {}
    # for post in main_page_news:
    #     posts[post] = PostPhoto.objects.filter(post__pk=post.pk).first()

    #Вывести ВСЕ объекты из БД
    # posts = Post.objects.all()[:3]
    posts = Post.objects.filter(publish_on_main_page=True)[:7]
    publications = []
    for post in posts:
        try:
            publications.append({'post': post, 'photo': PostPhoto.objects.get(post=post).image.url })
        except PostPhoto.DoesNotExist:
            publications.append({'post': post, 'photo': 'https://place-hold.it/500x300'})
    print('PUBLICACTIONS', publications)
    # main_page_articles = Article.objects.filter(
    #     publish_on_main_page=True).order_by('-published_date')[:3]

    # print(request.resolver_match)
    # print(request.resolver_match.url_name)

    content = {
        'title': title,
        'publications': publications
        # 'docs': docs,
        # 'articles': main_page_articles,
        # 'send_message_form': SendMessageForm(),
        # 'subscribe_form': SubscribeForm(),
        # 'ask_question_form': AskQuestionForm()
    }

    return render(request, 'mainapp/index.html', content)

def reestr(request):
    title = 'Реестр'

    content = {
        'title': title
    }
    return render(request, 'mainapp/reestr.html', content)

def doc(request):
    # documents= Document.objects.all()

    gac_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name='ССР3ГАЦ'))
    csp_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name='ССР3ЦСП'))
    acsm_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name='АЦСМ46'))
    acso_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name='АЦСО82'))
    acst_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name='АЦСТ90'))
    cok_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name='COK12'))


    content={
        "title": "doc",
        "ssr_3gac_documents": gac_documents,
        "ssr_3csp_documents": csp_documents,
        "acsm_46_documents": acsm_documents,
        "acso_82_documents": acso_documents,
        "acst_90_documents": acst_documents,
        "cok_12_documents": cok_documents,

    }
    return render(request, 'mainapp/doc.html', content)


# def details_news(request, pk=None):
#     post = Post.objects.get(pk=pk)
#     content= {
#         'title': 'Детальный просмотр',
#         'post': post
#     }
#     return render(request, 'mainapp/details_news.html', content)


def partners(request):
    return render(request, 'mainapp/partners.html')


def page_details(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    content = {
        'title': 'Детальный просмотр',
        'post': post,
    }
    return render(request, 'mainapp/page_details.html', content)

def cok(request):
    spks_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name="НПА СПКС")
    ).order_by('-created_date')
    spks_example_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name="Образцы документов СПКС")
    )
    content = {
        'title': 'cok_documets',
        'spks_documents': spks_documents,
        'spks_example_documents': spks_example_documents
    }
    return render(request, 'mainapp/cok.html', content)

def profstandarti(request):
    return render(request, 'mainapp/profstandarti.html')
def contacts(request):
    return render(request, 'mainapp/contacts.html')
def all_news(request):
    content = {
        'title': 'All news',
        'news': Post.objects.all().order_by('-published_date')[:9]
    }
    return render(request, 'mainapp/all_news.html', content)

def political(request):
    political_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name="НПА СПКС")
    ).order_by('-created_date')
    political_example_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name="Образцы документов СПКС")
    )
    content = {
        'title': 'political_documets',
        'political_documents': political_documents,
        'political_example_documents': political_example_documents
    }
    return render(request, 'mainapp/political.html', content)

def details_news(request, pk=None):

    return_link = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(publish_on_news_page=True).exclude(pk=pk)[:3]
    attached_images = PostPhoto.objects.filter(post__pk=pk)
    attached_documents = Document.objects.filter(post__pk=pk)
    post_content = {
        'post': post,
        'related_posts': related_posts,
        'images': attached_images,
        'documents': attached_documents,
    }

    return render(request, 'mainapp/details_news.html', post_content)