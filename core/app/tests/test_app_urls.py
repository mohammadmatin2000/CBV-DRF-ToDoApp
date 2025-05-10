from django.test import TestCase
from django.urls import reverse,resolve
from ..views import ListView,DeleteTaskView,UpdateTaskView

# ======================================================================================================================
class TestUrl(TestCase):
    def test_blog_index_url_resolve(self):
        url = reverse('blog:index-class')
        self.assertEqual(resolve(url).func.view_class,ListView)
    def test_blog_list_url_resolve(self):
        url = reverse('blog:post-list')
        self.assertEqual(resolve(url).func.view_class,UpdateTaskView)
    def test_blog_detail_url_resolve(self):
        url = reverse('blog:post-detail',kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class,DeleteTaskView)
# ======================================================================================================================