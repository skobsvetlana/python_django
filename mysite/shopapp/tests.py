import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Permission
from django.db.models import QuerySet
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers

from string import ascii_letters
from random import choices


class AddTwoNumbers(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'user_groups-fixture.json',
    ]

    def setUp(self) -> None:
        self.client.post(reverse("accounts:login"), {"username": "User2", "password": "zzzz2222"})
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:create_product"),
            {
                "name": self.product_name,
                "description": "test_product description",
                "quantity": 1,
                "price": 123.45,
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username="User2",
            password="zzzz2222,"
        )
        cls.product = Product.objects.create(
            name="Test product",
            quantity=1,
            price=123.45,
            created_by=cls.user
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):  ## dont work
    fixtures = [
        'products-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test1234")
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_products(self):
        # c = Client()
        # response = c.post("/accounts/login/", {"username": "User2", "password": "zzzz2222"})
        # response = c.get("/shop/products/")

        response = self.client.get(reverse("shopapp:products_list"))

        # for product in Product.objects.filter(archived=False).all():
        #     #self.assertEqual(response.status_code, 302) !!!!!!!!
        #     self.assertContains(response, product.name)

        # products = Product.objects.filter(archived=False).all()
        # products_resp = response.context["products"]
        # for p, p_resp in zip(products, products_resp):
        #     self.assertEqual(p.pk, p_resp.pk)

        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'users-fixture.json',
        'user_groups-fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products_export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "description": product.description,
                "quantity": product.quantity,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data
        )


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test1234")
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username="test",
            password="test1234",
        )
        view_order_permission = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(view_order_permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="Moscow",
            promocode="SALE",
            user=self.user,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_get_order(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopapp/order-details.html')

    def test_get_order_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertContains(response, "Order details")
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(self.order.pk, response.context["order"].pk)


class OrdersExportViewTestCase(TestCase):  ## dont work
    fixtures = [
        'products-fixture.json',
        'orders-fixture.json',
        "users-fixture.json",
        'user_groups-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_staff = User.objects.create(
            username="test_staff",
            password="test1234",
        )
        cls.user_staff.is_staff = True
        cls.user_staff.save()
        cls.user_not_staff = User.objects.create(
            username="test_not_staff",
            password="test1234",
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user_staff.delete()
        cls.user_not_staff.delete()

    def setUp(self) -> None:
        # self.user_staff = User.objects.create(
        #     username="test_staff",
        #     password="test1234",
        # )
        # self.user_staff.is_staff = True
        # self.user_staff.save()
        # self.user_not_staff = User.objects.create(
        #     username="test_not_staff",
        #     password="test1234",
        # )
        self.client.force_login(self.user_staff)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_export"))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Orders export")

    def test_orders_view_content(self):
        response = self.client.get(
            reverse("shopapp:orders_export"),
        )
        orders = Order.objects.order_by("pk").select_related("user").prefetch_related("products").all()
        expected_data = json.dumps(
            [
                {
                    "pk": order.pk,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,
                    "created_at": str(order.created_at),
                    "user": order.user.username,
                    "products": [product.name for product in order.products.all()],
                }
                for order in orders
            ]
        )
        export_orders_data = response.json()['orders']
        print("orders", expected_data)
        print("response.context", export_orders_data)
        self.assertJSONEqual(expected_data, export_orders_data)

    def test_orders_view_not_is_staff(self):
        self.client.logout()
        self.client.force_login(self.user_not_staff)

        response = self.client.get(reverse("shopapp:orders_export"))
        self.assertEqual(response.status_code, 403)
