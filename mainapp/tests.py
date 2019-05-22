from django.test import TestCase
from django.test import Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from mainapp.models import Post, Document, DocumentCategory
from http import HTTPStatus
from django.shortcuts import get_list_or_404
from mixer.backend.django import mixer
import random
# Create your tests here.

# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1+1, 3)



class MainPageTest(TestCase):
    # def setUp(self):
    def test_main_page_loads_without_errors(self):
        response = self.client.get(reverse('index'))
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Главная страница</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'mainapp/index.html')

    def test_can_create_and_publish_news(self):
        for i in range(3):
            mixer.blend(Post, publish_on_main_page=True)
        response = self.client.get(reverse('index'))
        self.assertTrue(len(response.context['basement_news']), 3)

    def test_can_open_news_by_details_url(self):
        posts = mixer.cycle(3).blend(Post, publish_on_main_page=True)
        for post in posts:
            url = reverse('details_news', kwargs={'pk': post.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.context['post'], Post))
            self.assertEqual(post.title, response.context['post'].title)
            self.assertTrue('related_posts' in response.context)
            self.assertTrue(post not in response.context['related_posts'])

    def test_can_create_link_holders_and_open_pages(self):
        post_center_info = mixer.blend(Post, url_code='CENTER_INFO', title="About us")
        response = self.client.get(reverse('index'))
        html = response.content.decode('utf8')
        self.assertTrue('About us' in html)
        details_response = self.client.get(reverse('details', kwargs={'pk': post_center_info.pk}))
        self.assertTrue(details_response.status_code, 200)
        details_html = details_response.content.decode('utf8')
        self.assertTrue(post_center_info.title in details_html)
        self.assertTemplateUsed(details_response, 'mainapp/page_details.html')





