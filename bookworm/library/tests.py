from django.test import TestCase
from library.models import Author, Book

class TestAuthor(TestCase):
    def setUp(self):
        Author.objects.create(firstname="bozorg", lastname="alavi", nationality="iranian")

    def test__str__(self):
        author = Author.objects.get(firstname="bozorg")
        self.assertEqual(author.__str__(), "bozorg alavi")
class TestBook(TestCase):    
        
    def setUp(self):
        a1 = Author.objects.create(firstname='abbas', lastname='maroufi', nationality='iranian')
        book = Book.objects.create(title='sale balva', genre='drama')
        book.author.add(a1)
        book.save()

    def test__str__(self):
        book = Book.objects.get(title='sale balva')
        self.assertEqual(book.__str__(), 'sale balva')