import datetime
import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError
from medicines.models import CategoryType, InventoryItem, InventoryStock, InventoryTransaction, PackagingType, SubcategoryType, UnitType
from users.models import CustomUser

def create_test_item(self):
    self.item = InventoryItem.objects.create(
        id=str(uuid.uuid4()),  # Ensure a valid UUID
        category=CategoryType.ANTACIDS,
        subcategory=SubcategoryType.ANTACID,
        item_name="Magnesium Hydroxide",
        brand_name="Phillips' Milk of Magnesia",
        generic_name="Magnesium Hydroxide",
        dosage_form="Liquid",
        strength_per_size="400mg/5ml",
        packaging=PackagingType.BOTTLE,
        quantity=120,
        unit_size=UnitType.ML,
    )

def create_test_stock(self):
    self.stocks = InventoryStock.objects.create(
        item=self.item,
        count=5,
        expiration_date=datetime.date.today(),
        date_of_delivery=datetime.date.today(),
    )

class ItemTestCase(TestCase):
    def setUp(self):
        """Set up an inventory item for testing"""
        create_test_item(self)
        create_test_stock(self)

    def test_item_exists(self):
        """Test if an item exists in the database"""
        item = InventoryItem.objects.get(item_name="Magnesium Hydroxide")
        self.assertIsNotNone(item)

    def test_default_stock_value(self):
        """Ensure stocks are initialized correctly"""
        self.assertEqual(self.stocks.count, 5)
    
    def test_invalid_unit_type_raise_error(self):
        with self.assertRaises(ValidationError):
            InventoryItem.objects.create(
                category=CategoryType.ANTACIDS,
                subcategory=SubcategoryType.ANTACID,
                item_name="Magnesium Hydroxide",
                brand_name="Phillips' Milk of Magnesia",
                generic_name="Magnesium Hydroxide",
                dosage_form="Liquid",
                strength_per_size="400mg/5ml",
                packaging=PackagingType.BOTTLE,
                quantity=120,
                unit_size="lkjsdf",
            )

    def test_invalid_category_type_raise_error(self):
        with self.assertRaises(ValidationError):
            InventoryItem.objects.create(
                category="SOME INVALID CATEOGRY",
                subcategory=SubcategoryType.ANTACID,
                item_name="Magnesium Hydroxide",
                brand_name="Phillips' Milk of Magnesia",
                generic_name="Magnesium Hydroxide",
                dosage_form="Liquid",
                strength_per_size="400mg/5ml",
                packaging=PackagingType.BOTTLE,
                quantity=120,
                unit_size=UnitType.EACH,  
            )
    def test_invalid_subcategory_type_raise_error(self):
        with self.assertRaises(ValidationError):
            InventoryItem.objects.create(
                category=CategoryType.ANTACIDS,
                subcategory="SOME INVALID SUBCATEGORY",
                item_name="Magnesium Hydroxide",
                brand_name="Phillips' Milk of Magnesia",
                generic_name="Magnesium Hydroxide",
                dosage_form="Liquid",
                strength_per_size="400mg/5ml",
                packaging="Bottle",
                quantity=120,
                unit_size=UnitType.EACH,  
            )

    def test_invalid_packaging_type_raise_error(self):
        with self.assertRaises(ValidationError):
            InventoryItem.objects.create(
                category="SOME INVALID CATEOGRY",
                subcategory=SubcategoryType.ANTACID,
                item_name="Magnesium Hydroxide",
                brand_name="Phillips' Milk of Magnesia",
                generic_name="Magnesium Hydroxide",
                dosage_form="Liquid",
                strength_per_size="400mg/5ml",
                packaging="INVALID LPACKAGING TYPE",
                quantity=120,
                unit_size=UnitType.EACH,  
            )

class TransactionTestCase(TestCase):
    def setUp(self):
        """Set up an inventory item and user for transactions"""
        create_test_item(self)
        create_test_stock(self)
        self.user = CustomUser.objects.create_user(
            email="test_email@example.com",
            password="1234"
        )

    def test_item_modified(self):
        """Test that adding stock increases the item's stock count"""
        InventoryTransaction.objects.create(
            item_stock=self.stocks,
            user=self.user,
            quantity=5,
            transaction_type=InventoryTransaction.ADD,
        )
        modified_stock = InventoryStock.objects.get(item=self.item)
        self.assertEqual(modified_stock.count, 10)

    def test_transaction_removes_stock_correctly(self):
        """Test that removing stock decreases the item's stock count"""
        InventoryTransaction.objects.create(
            item_stock=self.stocks,
            user=self.user,
            quantity=3,
            transaction_type=InventoryTransaction.REMOVE,
        )
        modified_stock = InventoryStock.objects.get(item=self.item)
        self.assertEqual(modified_stock.count, 2)

    def test_transaction_fails_when_insufficient_stock(self):
        """Test that removing more stock than available raises an error"""
        with self.assertRaises(ValueError) as e:
            InventoryTransaction.objects.create(
                item_stock=self.stocks,
                user=self.user,
                quantity=10,  # More than available stocks
                transaction_type=InventoryTransaction.REMOVE,
            )
        self.assertEqual(str(e.exception), "Not enough stock available")

    def test_multiple_transactions_affect_stock_correctly(self):
        """Test multiple transactions updating stock properly"""
        InventoryTransaction.objects.create(
            item_stock=self.stocks,
            user=self.user,
            quantity=2,
            transaction_type=InventoryTransaction.ADD,
        )
        InventoryTransaction.objects.create(
            item_stock=self.stocks,
            user=self.user,
            quantity=3,
            transaction_type=InventoryTransaction.REMOVE,
        )
        modified_stock = InventoryStock.objects.get(item=self.item)
        self.assertEqual(modified_stock.count, 4)  # 5 + 2 - 3 = 4

    def test_transaction_modification_changes_stock(self):
        transaction = InventoryTransaction.objects.create(
            item_stock=self.stocks,
            user=self.user,
            quantity=2,
            transaction_type=InventoryTransaction.ADD,
        )
        transaction.quantity = 5
        transaction.save()
        
        modified_stocks = InventoryStock.objects.get(id=self.stocks.id)
        self.assertEqual(modified_stocks.count, 5+5)

        transaction.quantity = 7
        transaction.save()
        modified_stocks = InventoryStock.objects.get(id=self.stocks.id)
        self.assertEqual(modified_stocks.count, 5+7)

    def test_transaction_deletion_changes_stock(self):
        transaction = InventoryTransaction.objects.create(
            item_stock=self.stocks,
            user=self.user,
            quantity=2,
            transaction_type=InventoryTransaction.ADD,
        )
        transaction.delete()

        modified_stock = InventoryStock.objects.get(id=self.stocks.id)
        self.assertEqual(modified_stock.count, 5)

    def test_item_deletion_cascades(self):
        transaction = InventoryTransaction.objects.create(
            item_stock=self.stocks,
            user=self.user,
            quantity=2,
            transaction_type=InventoryTransaction.ADD,
        )
        self.item.delete()
        self.assertEqual(
            0,
            InventoryTransaction.objects.all().count(),
        )

    def test_not_enough_stock_error_raise(self):
        with self.assertRaises(ValueError):
            InventoryTransaction.objects.create(
                item_stock=self.stocks,
                user=self.user,
                quantity=10,
                transaction_type=InventoryTransaction.REMOVE,
            )
    
    def test_invalid_transaction_type_raise_error(self):
        with self.assertRaises(ValueError):
            InventoryTransaction.objects.create(
                item_stock=self.stocks,
                user=self.user,
                quantity=1,
                transaction_type="asdf",
            )

    def test_stock_cannot_be_negative_due_to_transactions(self):
        transaction = InventoryTransaction.objects.create(
            item_stock=self.stocks,
            user=self.user,
            quantity=2,
            transaction_type=InventoryTransaction.REMOVE,
        )
        transaction.quantity = 10
        with self.assertRaises(ValueError):
            transaction.save()
            transaction.quantity = -2
            transaction.save()
    

class InventoryStockTestCase(TestCase):
    def setUp(self):
        """Set up an inventory item for testing"""
        create_test_item(self)
        create_test_stock(self)

    def deletion_of_item_cascades(self):
        self.assertEqual(
            InventoryStock.objects.all().count(),
            1
        )
        self.item.delete()
        self.assertEqual(
            InventoryStock.objects.all().count(),
            0
        )
    def test_cannot_add_expired_stock(self):
        """Ensure that adding stock with a past expiration date raises an error"""
        with self.assertRaises(ValidationError):
            InventoryStock.objects.create(
                item=self.item,
                expiration_date=datetime.date.today() - datetime.timedelta(days=1),
                count=5
            )

    def test_can_update_expired_stock(self):
        """Ensure modifying stock for an expired item is allowed"""
        self.stocks.expiration_date = datetime.date.today() - datetime.timedelta(days=1)
        self.stocks.count = 5
        self.stocks.save()
        self.assertEqual(InventoryStock.objects.get(id=self.stocks.id).count, 5)

    def test_cannot_have_duplicate_expiration_date(self):
        """Ensure that adding duplicate stock entries for the same expiration date raises an error"""
        with self.assertRaises(Exception):
            InventoryStock.objects.create(
                item=self.item,
                expiration_date=self.stock.expiration_date,
                count=5
            )


