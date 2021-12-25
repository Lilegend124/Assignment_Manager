from django.test import TestCase, Client
from django.test import TestCase
from .models import To_Do_Item, User, Class_Item, Document
import load_classes
from django.shortcuts import render, get_object_or_404

class DummyTest(TestCase):
    def test_addition(self):
        a = 1
        b = 1
        assert(a==b)

class LoggedIn(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", email="user1@gmail.com")
        user.set_password("password")
        user.save()
    
    def test_login(self):
        c = Client()
        self.assertTrue(c.login(username="testuser", password="password"))

class Test_Creation_To_Do(TestCase):
    def setUp(self):
        user = User.objects.create(username="foo", email="user1@gmail.com")
        user.set_password("bar")
        user.save()
        To_Do_Item.objects.create(title="Item 1", content="Item 1 content", author = user)
    def test_number_of_to_do_items_increased(self):
        self.assertEqual(len(To_Do_Item.objects.all()),1)

class Test_To_Do_Redirects(TestCase):
    def setUp(self):
        """
        Create user/users and objects wanting to test.
        """
        # creating users
        user1 = User.objects.create(username="user1", email="user1@gmail.com")
        user1.set_password("user1")
        user1.save()

        user2 = User.objects.create(username="user2", email="user2@gmail.com")
        user2.set_password("user2")
        user2.save()

        # creating three objects
        # Item x.y means the y'th item of user x
        To_Do_Item.objects.create(title="Item 1.1", content="Item 1.1 content", author = user1)
        To_Do_Item.objects.create(title="Item 1.2", content="Item 1.1 content", author = user1)
        To_Do_Item.objects.create(title="Item 2.1", content="Item 2.1 content", author = user2)

    def test_login_access_allowed(self):
        c = Client()
        c.login(username="user1",password="user1")
        
        response = c.get('/day', follow=True) # make sure to have follow=True
        self.assertEqual(response.status_code, 200)
        
        response = c.get('/to_do/create', follow=True)
        self.assertEqual(response.status_code, 200)
        
        c.logout()

        c2 = Client()
        c2.login(username="user2", password="user2")
        response = c2.get('/day', follow=True)
        self.assertIn('Item 2.1', response.content.decode())

    def test_no_login_access_denied(self):
        """
        If not legged in go to the login page.
        """
        c = Client()
        response = c.get('/day', follow=True)
        self.assertIn('Sign In', response.content.decode())

class Test_Classes(TestCase):
    def setUp(self):
        """
        Create user/users and objects wanting to test.
        """
        # creating users
        user1 = User.objects.create(username="user1", email="user1@gmail.com")
        user1.set_password("user1")
        user1.save()

        user2 = User.objects.create(username="user2", email="user2@gmail.com")
        user2.set_password("user2")
        user2.save()
        load_classes.main(1000, testing=True)
        Class_to_add = get_object_or_404(Class_Item, pk = 1)
        self.class1_name = Class_to_add.class_title.split()[0]
        Class_to_add2 = get_object_or_404(Class_Item, pk = 20)
        self.class2_name = Class_to_add2.class_title.split()[0]
        user1.classes.add(Class_to_add)

    def test_user_add_class(self):
        c = Client()
        c.login(username="user1",password="user1")

        response = c.get('/classes/add', follow=True)
        self.assertIn('AAS', response.content.decode())

        response = c.get('/classes', follow=True) # make sure to have follow=True
        self.assertIn(self.class1_name, response.content.decode())
        self.assertNotIn(self.class2_name, response.content.decode())
        
        c.logout()

        c2 = Client()
        c2.login(username="user2",password="user2")
        response = c2.get('/classes', follow=True)
        self.assertNotIn(self.class1_name, response.content.decode())
        self.assertNotIn(self.class2_name, response.content.decode())

class Test_File_Upload(TestCase):
    def setUp(self):
        """
        Create user/users and objects wanting to test.
        """
        # creating users
        user1 = User.objects.create(username="user1", email="user1@gmail.com")
        user1.set_password("user1")
        user1.save()

        user2 = User.objects.create(username="user2", email="user2@gmail.com")
        user2.set_password("user2")
        user2.save()
        load_classes.main(1000, testing=True)
        Class_to_add = get_object_or_404(Class_Item, pk = 1)
        Class2 = get_object_or_404(Class_Item, pk = 2)
        user1.classes.add(Class_to_add)
        Document.objects.create(name="Doc1", doc='test.py', class_item=Class_to_add, author=user1)
        Document.objects.create(name="Doc2", doc='test2.py', class_item=Class2, author=user1)

    def test_user_add_class(self):
        c = Client()
        c.login(username="user1",password="user1")

        response = c.get('/classes/1', follow=True) # make sure to have follow=True
        self.assertIn('Doc1', response.content.decode())
        self.assertNotIn('Doc2', response.content.decode())
        
        c.logout()


class Test_Google(TestCase):
    def setUp(self):
        return super().setUp()
    def test_calendar_insert(self):
        assert(1==1)
