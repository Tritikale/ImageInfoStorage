from django.test import TestCase, Client
from django.core.files.images import ImageFile
from tempfile import TemporaryFile
from PIL import Image, ImageChops

from .models import Page
from .views import create_image, create_image_name, create_password, index, show_page


# Create your tests here.
def difference_images(img1, img2):
    image_1 = Image.open(img1)
    image_2 = Image.open(img2)
    result = ImageChops.difference(image_1, image_2).getbbox()
    image_1.close()
    image_2.close()
    if result is None:
        return True
    else:
        return False


class PageTestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        with TemporaryFile(mode='w+b') as file:
            create_image('text_info', file)
            Page.objects.create(image=ImageFile(file, name="test.png"), password='12345', time=2)

    def test_add_page(self):
        page = Page.objects.get(image='images/test.png')
        self.assertEqual('images/test.png', page.image.name)
        self.assertEqual('12345', page.password)
        self.assertEqual(2, page.time)

    def test_main_page_response(self):
        response = self.client.get('')
        self.assertEqual(200, response.status_code)

    def test_main_page_converting_text_to_image(self):
        self.client.post('', data={'text_info': 'sometext'})
        page = Page.objects.get(id=2)
        with TemporaryFile(mode='w+b') as file:
            create_image('sometext', file)
            self.assertTrue(difference_images(file, page.image))
        img_name = str(page.image.url)
        page.image.storage.delete(img_name[7:])
        page.delete()

    def test_main_page_invalid_input(self):
        response = self.client.post('', data={'text_info': '   '})
        self.assertTrue('error_message' in response.context)
        self.assertEqual('input is not valid', response.context.get('error_message'))

    def test_show_page_response(self):
        response = self.client.get('/test')
        self.assertEqual(200, response.status_code)

    def test_show_page_password(self):
        response = self.client.post('/test', data={'text_info': '12345'})
        self.assertTrue('page' in response.context)
        self.assertTrue('message' in response.context)

    def test_show_page_wrong_password(self):
        response = self.client.post('/test', data={'text_info': 'wrong'})
        self.assertTrue('error_message' in response.context)
        self.assertEqual('password is incorrect', response.context.get('error_message'))

    def test_show_page_invalid_input(self):
        response = self.client.post('/test', data={'text_info': '   '})
        self.assertTrue('error_message' in response.context)
        self.assertEqual('input is not valid', response.context.get('error_message'))

    def test_show_page_time_changer(self):
        response = self.client.post('/test', data={'text_info': '12345'})
        page = response.context.get('page')
        self.assertEqual(1, page.time)
        response = self.client.post('/test', data={'text_info': '12345'})
        page = response.context.get('page')
        self.assertEqual(0, page.time)

    def test_show_page_deleted(self):
        self.client.post('/test', data={'text_info': '12345'})
        self.client.post('/test', data={'text_info': '12345'})
        response = self.client.post('/test', data={'text_info': '12345'})
        self.assertTrue('message' in response.context)
        self.assertEqual('Page was deleted', response.context.get('message'))

    def test_clear_files(self):
        page = Page.objects.get(image='images/test.png')
        img_name = str(page.image.url)
        page.image.storage.delete(img_name[7:])
        page.delete()
