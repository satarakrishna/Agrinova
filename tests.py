
# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import CropAdvice
from django.contrib.auth.models import User
import json

# ---------------------- MODELS TESTS ----------------------
class CropAdviceModelTest(TestCase):
    def setUp(self):
        self.crop = CropAdvice.objects.create(
            crop="Wheat",
            region="Rabi Region",
            what_to_do="Prepare soil",
            how_to_do="Plow and fertilize",
            when_to_do="December"
        )

    def test_crop_creation(self):
        """Test that a CropAdvice object is created correctly"""
        self.assertEqual(self.crop.crop, "Wheat")
        self.assertEqual(str(self.crop), "Wheat (Rabi Region)")

# ---------------------- VIEWS TESTS ----------------------
class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_redirect_for_anonymous(self):
        """Anonymous users should be redirected to login"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_static_pages(self):
        """Test rendering of static pages"""
        pages = [
            "about1", "about2", "about3", "knowledge", "weather", "soil",
            "chome", "cweather", "csoils", "cedu", "cpest", "cmarket",
            "cfungal", "cgrowth"
        ]
        for page in pages:
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 200)

# ---------------------- AI CHATBOT TEST ----------------------
class AIChatTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_chat_page(self):
        """GET request returns 200"""
        response = self.client.get(reverse('ai_chat'))
        self.assertEqual(response.status_code, 200)

    def test_post_chat_no_message(self):
        """POST with no message returns error"""
        response = self.client.post(reverse('ai_chat'), {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("No message provided", response.json().get("error", ""))

from django.contrib.auth.models import User
from .models import CropAdvice
import json

class IntegrationTestCase(TestCase):

    # 1️⃣ Login → Dashboard Integration
    def test_login_and_index_access(self):
        user = User.objects.create_user(username='farmer', password='12345')
        login = self.client.login(username='farmer', password='12345')
        self.assertTrue(login)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # 2️⃣ Anonymous User Redirect Integration
    def test_anonymous_redirect(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    # 3️⃣ Model + Database Integration
    def test_crop_advice_database_integration(self):
        CropAdvice.objects.create(
            crop="Wheat",
            region="North",
            what_to_do="Prepare soil",
            how_to_do="Use tractor plowing",
            when_to_do="Before sowing"
        )

        crop = CropAdvice.objects.get(crop="Wheat")
        self.assertEqual(crop.region, "North")

    # 4️⃣ AI Chat View Integration (POST Request)
    def test_ai_chat_post_request(self):
        data = {
            "message": "How to grow rice?",
            "history": []
        }

        response = self.client.post(
            reverse('ai_chat'),
            data=json.dumps(data),
            content_type='application/json'
        )

        # Even if AI server not running, view should respond properly
        self.assertIn(response.status_code, [200, 500])

    # 5️⃣ Static Page Integration
    def test_static_pages_load(self):
        pages = ['about1', 'knowledge', 'soil']
        for page in pages:
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 200)