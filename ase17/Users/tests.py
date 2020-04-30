from django.test import TestCase
from Users.models import Profile, User
from .forms import RegistrationForm, ProfileRegistrationForm, ProfileUpdateForm
from django.test import Client
from django.urls import reverse



class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_object = User(username='pavan', email='mail@gmail.com')
        user_object.set_password('testing321')
        user_object.save()

        profile_object = Profile.objects.create(user=user_object, phone_no='1234567891', address='Sricity',
                                                card_no='1234567891011121')

    def test_check_for_creation(self):
        self.assertTrue(Profile.objects.filter(user=User.objects.get(username='pavan')).exists())



class RegisterTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous_ping(self):
        #print('\nregister testing\n')
        response = self.client.get('/register/')

        self.assertEqual(response.status_code, 200)


class RegisterUrlTest(TestCase):

    def setUp(self):
        self.user_object = User(username='pavan',email='mail@gmail.com')
        self.user_object.set_password('testing321')
        self.user_object.save()
        #self.createduser = Profile.objects.create(user=user_object, phone_no='1234567891', address='Sricity', card_no='1234567891011121')
        self.client = None
        self.request_url = '/register/'
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous(self):
        #print('register unknown testing\n')
        #print(self.user_object.password)
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)

    def test_after_login(self):
        #print('register authenticated testing\n')
        self.client = Client()
        self.client.login(username='self.user_object.username', password='self.user_object.password')
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id(self):
        #print('register authenticated_random testing\n')
        self.client = Client()
        self.client.login(username='self.user_object.username', password='self.user_object.password')
        response = self.client.get('/register/blahblah')
        self.assertEqual(response.status_code, 404)



class LoginUrlTest(TestCase):

    def setUp(self):
        self.user_object = User(username='pavan',email='mail@gmail.com')
        self.user_object.set_password('testing321')
        self.user_object.save()
        self.createduser = Profile.objects.create(user=self.user_object, phone_no='1234567891', address='Sricity', card_no='1234567891011121')
        #self.createduser = User.objects.create_user(username="testnormaluser", password="Test Hello World")
        self.client = None


    def test_dashboard(self):
        self.client = Client()
        self.request_url = reverse('dashboard')
        response = self.client.get(self.request_url)
        #print(response.status_code)
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)

    def test_create_auction(self):
        self.client = Client()
        self.request_url = reverse('create-auction')
        response = self.client.get(self.request_url)
        #print(response)
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)

    def test_joined_auction(self):
        self.client = Client()
        self.request_url = '/dashboard/participated-auctions/'
        response = self.client.get(self.request_url)
        #print(response)
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)

    def test_created_auction(self):
        self.client = Client()
        self.request_url = '/dashboard/created-auctions/'
        response = self.client.get(self.request_url)
        #print(response)
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)

    def test_join_in_auction(self):
        self.client = Client()
        self.request_url = '/join/332'
        response = self.client.get(self.request_url)
        #print(response)?next=/join/33
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)

    #after login
    def test_dashboard_login(self):
        self.client = Client()
        self.client.login(username=self.user_object.username, password=self.user_object.password)
        self.request_url = reverse('dashboard')
        response = self.client.get(self.request_url)
        #print(response.status_code)
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)
        # self.assertRedirects(response, expected_url='/dashboard/')

    def test_create_auction_login(self):
        self.client = Client()
        self.client.login(username=self.user_object.username, password=self.user_object.password)
        self.request_url = reverse('create-auction')
        response = self.client.get(self.request_url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)
        # self.assertRedirects(response, expected_url='/create-auction/')

    def test_joined_auction_login(self):
        self.client = Client()
        self.client.login(username=self.user_object.username, password=self.user_object.password)
        self.request_url = '/dashboard/participated-auctions/'
        response = self.client.get(self.request_url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)
        #self.assertRedirects(response, expected_url='/dashboard/participated-auctions/')

    def test_created_auction_login(self):
        self.client = Client()
        self.client.login(username=self.user_object.username, password=self.user_object.password)
        self.request_url = '/dashboard/created-auctions/'
        response = self.client.get(self.request_url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)
        #self.assertRedirects(response, expected_url='/dashboard/created-auctions/')

    def test_join_in_auction_login(self):
        self.client = Client()
        self.client.login(username=self.user_object.username, password=self.user_object.password)
        self.request_url = '/join/332'
        response = self.client.get(self.request_url)
        #print(response)?next=/join/33
        self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)
        #self.assertRedirects(response, expected_url='/join/332')


class TestRegisterForm(TestCase):

    # def setUp(self):
    #     self.user = User.objects.create(username="testuser", email="mailuser@gmail.com", password="testing321")

    def test_registration_form(self):
        form_instance = RegistrationForm(data={
            "username": "Sample_User",
            "password": "testing321",
            "confirm_password": "testing321",
            "email": "mail@gmail.com",
        })
        self.assertEqual(form_instance.is_valid(), True)

        register = form_instance.save(commit=False)

        register.save()

        model_instance = User.objects.get(username="Sample_User")
        self.assertEqual(model_instance.username, "Sample_User")
        self.assertEqual(model_instance.email, "mail@gmail.com")


    # def test_registration_user_form(self):
    #     form_instance = RegistrationForm(data={
    #         "username": "Sample_User",
    #         "password": "testing321",
    #         "confirm_password": "testing321",
    #         "email": "mail@gmail.com",
    #     })
    #     self.assertEqual(form_instance.is_valid(), False)
    #
    #     register = form_instance.save(commit=False)
    #
    #     register.save()
    #     self.assertEqual(form_instance.is_valid(), False)
    #     self.assertEqual(form_instance.errors.get("user"), None)
    #
    #     model_instance = User.objects.get(username="Sample_User")
    #     self.assertEqual(model_instance.username, "Sample_User")
    #     self.assertEqual(model_instance.email, "mail@gmail.com")





    # #after login
    # def test_authenticated(self):
    #     self.client = Client()
    #     self.client.login(username=self.user_object.username, password=self.user_object.password)
    #     self.request_url = reverse('dashboard')
    #     response = self.client.get(self.request_url)
    #     # self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, expected_url='/accounts/login/?next=' + self.request_url)
    #     # self.assertRedirects(response, expected_url='/dashboard/')
    #
    # #after login
    # def test_authenticated_ping(self):
    #     self.client = Client()
    #     self.client.login(username=self.user_object.username, password=self.user_object.password)
    #     response = self.client.get(self.request_url)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_authenticated_random_id_ping(self):
    #     self.client = Client()
    #     self.client.login(username=self.user_object.username, password=self.user_object.password)
    #     response = self.client.get('wrongurlabc')
    #     self.assertEqual(response.status_code, 404)




#     #class TestProfileRegistrationForm(TestCase):
#
#     def setUp(self):
#         self.user_object = User(username='pavan', email='mail@gmail.com')
#         self.user_object.set_password('testing321')
#         self.user_object.save()
#
#     def test_profile_registration_form(self):
#         form_instance = ProfileRegistrationForm(data={
#                     "user": self.user_object,
#                     "phone_no": "4583982347",
#                     "address": "go to hell",
#                     "card_no": "8263543986534872",
#                 })
#         self.assertEqual(form_instance.is_valid(), True)
#
#         register = form_instance.save(commit=False)
#
#         register.save()
#         model_instance = Profile.objects.get(user="pavan")
#         self.assertEqual(model_instance.phone_no, "4583982347")
#         self.assertEqual(model_instance.address, "go to tada"