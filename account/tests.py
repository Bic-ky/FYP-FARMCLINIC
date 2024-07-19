# from django.test import TestCase
# from chat.models import Thread, ChatMessage
# from account.models import User
# from datetime import datetime

# class ThreadManagerTestCase(TestCase):
#     def test_by_user(self):
#         # Create two users
#         user1 = User.objects.create(phone_number="1234567890", password="testpassword1")
#         user2 = User.objects.create(phone_number="9876543210", password="testpassword2")

#         thread = Thread.objects.create(first_person=user1, second_person=user2)
#         threads = Thread.objects.by_user(user=user1)
#         self.assertIn(thread, threads)

# class ThreadTestCase(TestCase):
#     def test_thread_creation(self):

#         user1 = User.objects.create(phone_number="1234567890", password="testpassword1")
#         user2 = User.objects.create(phone_number="9876543210", password="testpassword2")

#         thread = Thread.objects.create(first_person=user1, second_person=user2)
        

#         self.assertIsNotNone(thread)
#         self.assertEqual(thread.first_person, user1)
#         self.assertEqual(thread.second_person, user2)

# class ChatMessageTestCase(TestCase):
#     def test_chat_message_creation(self):
#         user = User.objects.create(phone_number="1234567890", password="testpassword")
#         thread = Thread.objects.create(first_person=user, second_person=user)
#         message = "Test message"
#         chat_message = ChatMessage.objects.create(thread=thread, user=user, message=message)
        
#         self.assertIsNotNone(chat_message)
#         self.assertEqual(chat_message.thread, thread)
#         self.assertEqual(chat_message.user, user)
#         self.assertEqual(chat_message.message, message)
#         self.assertIsInstance(chat_message.timestamp, datetime)




from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from account.forms import RegistrationForm

class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_post(self):
        data = {
            'phone_number': '1234567890',
            'role': '1',
            'full_name': 'Ram Hari',
            'email': 'ram@example.com',
            'password': 'testpassword',
            'address': '123 Street',
            'country': 'Nepal',
            'city': 'Kathmandu',
            'latitude': '27.7172',
            'longitude': '85.3240'
        }

        response = self.client.post(reverse('account:register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(phone_number='1234567890').exists())

    def test_register_get(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)
