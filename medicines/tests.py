import datetime
from django.test import TestCase

from medicines.models import InventoryItem, InventoryTransaction
from users.models import CustomUser

# Create your tests here.
item_id = "123456"
class ItemTestCase(TestCase):
    def setUp(self):
        InventoryItem.objects.create(
            id=item_id,
            category="Antacids",
            subcategory="Antacid",
            item_name="Magnesium Hydroxide",
            brand_name="Phillips' Milk of Magnesia",
            generic_name="Magnesium Hydroxide",
            dosage_form="Liquid",
            strength_per_size="400mg/5ml",
            packaging="Bottle",
            quantity=120,
            unit_size="ml",
            date_of_delivery=datetime.date.today(),
            expiration_date=datetime.date.today(),
            stocks=5 
        )
        return super().setUp()
    def test_item_exists(self):
        item = InventoryItem.objects.get(item_name="Magnesium Hydroxide")
        self.assertTrue(item)

class TransactionTestCase(TestCase):
    def setUp(self):
        self.item = InventoryItem.objects.create(
            id=item_id,
            category="Antacids",
            subcategory="Antacid",
            item_name="Magnesium Hydroxide",
            brand_name="Phillips' Milk of Magnesia",
            generic_name="Magnesium Hydroxide",
            dosage_form="Liquid",
            strength_per_size="400mg/5ml",
            packaging="Bottle",
            quantity=120,
            unit_size="ml",
            date_of_delivery=datetime.date.today(),
            expiration_date=datetime.date.today(),
            stocks=5 
        )
        self.user = CustomUser.objects.create_user(
            "test_email",
            "1234",
        )
        
        return super().setUp()

    
    def test_item_modified(self):
        InventoryTransaction.objects.create(
            item=self.item,
            user=self.user,
            quantity=5,
            transaction_type="add",
        )
        modified_item = InventoryItem.objects.get(id=item_id)
        self.assertEqual(
            modified_item.stocks, 
            10,
        )
