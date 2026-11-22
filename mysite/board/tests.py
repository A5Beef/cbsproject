from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Message


class MessagingTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="password")
        self.bob = User.objects.create_user(username="bob", password="password")
        self.other = User.objects.create_user(username="other", password="password")

    def test_sent_messages_only_show_current_users_messages(self):
        sent = Message.objects.create(
            sender=self.alice,
            recipient=self.bob,
            content="Hello Bob",
        )
        Message.objects.create(
            sender=self.bob,
            recipient=self.alice,
            content="Hello Alice",
        )

        self.client.force_login(self.alice)
        response = self.client.get(reverse("sent_messages"))

        self.assertContains(response, "To: bob")
        self.assertNotContains(response, "To: alice")
        self.assertContains(response, "Hello Bob")
        self.assertNotContains(response, "Hello Alice")

    def test_message_detail_is_available_to_sender_and_recipient(self):
        message = Message.objects.create(
            sender=self.alice,
            recipient=self.bob,
            content="Conversation message",
        )

        self.client.force_login(self.alice)
        sender_response = self.client.get(
            reverse("message_detail", args=[message.id])
        )
        self.assertEqual(sender_response.status_code, 200)
        self.assertContains(sender_response, "Conversation with bob")

        self.client.force_login(self.bob)
        recipient_response = self.client.get(
            reverse("message_detail", args=[message.id])
        )
        self.assertEqual(recipient_response.status_code, 200)
        self.assertContains(recipient_response, "Conversation with alice")

    def test_message_detail_rejects_unrelated_user(self):
        message = Message.objects.create(
            sender=self.alice,
            recipient=self.bob,
            content="Private",
        )

        self.client.force_login(self.other)
        response = self.client.get(reverse("message_detail", args=[message.id]))

        self.assertEqual(response.status_code, 404)

    def test_message_detail_includes_both_sides_of_conversation(self):
        sent = Message.objects.create(
            sender=self.alice,
            recipient=self.bob,
            content="First",
        )
        Message.objects.create(
            sender=self.bob,
            recipient=self.alice,
            content="Second",
        )
        Message.objects.create(
            sender=self.alice,
            recipient=self.other,
            content="Unrelated",
        )

        self.client.force_login(self.alice)
        response = self.client.get(reverse("message_detail", args=[sent.id]))

        self.assertContains(response, "First")
        self.assertContains(response, "Second")
        self.assertNotContains(response, "Unrelated")
