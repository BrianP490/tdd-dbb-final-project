# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db, DataValidationError
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #
    def test_read_a_product(self):
        """Tests reading a product"""
        # Create a product instance
        inst = ProductFactory()
        inst.id = None
        inst.create()   # The instance will get a new ID

        self.assertIsNot(inst.id, None)

        found_product = Product.find(inst.id)
        # Assert the properties of the found product match with the original instance
        self.assertEqual(found_product.name, inst.name)
        self.assertEqual(found_product.description, inst.description)
        self.assertEqual(found_product.price, inst.price)
        self.assertEqual(found_product.available, inst.available)
        self.assertEqual(found_product.category, inst.category)

    def test_update_a_product_error(self):
        """It should test updating a product and raising error"""
        inst = ProductFactory()
        inst.id = None
        inst.create()

        inst.id = None
        with self.assertRaises(DataValidationError):
            inst.update()

    def test_update_a_product(self):
        """It should test updating a product"""
        inst = ProductFactory()
        inst.id = None
        inst.create()
        first_id = inst.id  # save new ID

        # Updating the description
        inst.description = "This is just a test"
        inst.update()
        self.assertEqual(inst.id, first_id)
        self.assertEqual(inst.description, "This is just a test")

        all_products = Product.all()
        # Check fetched data
        assert len(all_products) == 1
        self.assertEqual(all_products[0].id, first_id)
        self.assertEqual(all_products[0].description, "This is just a test")

    def test_delete_a_product(self):
        """It should delete a Product"""
        inst = ProductFactory()
        inst.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        inst.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should list all products and verify consistency"""
        # Verify that the products list is empty
        products = Product.all()
        self.assertEqual(len(products), 0)

        for _ in range(5):
            inst = ProductFactory()
            inst.create()
        # Verify that 5 products remain
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_product_by_name(self):
        """It should find a product by name"""
        # Verify that the products list is empty
        products = Product.all()
        self.assertEqual(len(products), 0)

        for _ in range(5):
            inst = ProductFactory()
            inst.create()

        products = Product.all()
        first_prod_name = products[0].name

        # Count the number of products with the same name
        expected_occur = 0
        for inst in products:
            if inst.name == first_prod_name:
                expected_occur += 1

        products_matching_name = Product.find_by_name(first_prod_name)
        actual_occur = products_matching_name.count()
        self.assertEqual(actual_occur, expected_occur)

        # Assert that each products name matches the expected namd

        for prod in products_matching_name:
            self.assertEqual(prod.name, first_prod_name)

    def test_find_by_availability(self):
        """It should find products by availability"""
        # Populate the products
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        first_prod_target = products[0].available

        # Count the number of products with the same availability
        expected_occur = 0
        for inst in products:
            if inst.available == first_prod_target:
                expected_occur += 1

        matches = Product.find_by_availability(first_prod_target)
        actual_occur = matches.count()
        self.assertEqual(actual_occur, expected_occur)

        # Assert that each products name matches the expected namd

        for prod in matches:
            self.assertEqual(prod.available, first_prod_target)

    def test_find_by_category(self):
        """It should find products by category"""
        # Populate the products
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        first_prod_target = products[0].category

        # Count the number of products with the same category
        expected_occur = 0
        for inst in products:
            if inst.category == first_prod_target:
                expected_occur += 1

        matches = Product.find_by_category(first_prod_target)
        actual_occur = matches.count()
        self.assertEqual(actual_occur, expected_occur)

        # Assert that each products name matches the expected namd

        for prod in matches:
            self.assertEqual(prod.category, first_prod_target)

    def test_deserialize_missing_data(self):
        """It should test deserializing a product and raising error"""
        inst = ProductFactory()
        
        # Missing 'name' will cause a KeyError, which should be converted to DataValidationError
        data = {
            "name": "tool",
            "description": "my product",
            "price": ["10.50"],
            "available": True,
            "category": "CLOTHES"
        }
        with self.assertRaises(ValueError):
            inst.deserialize(data)