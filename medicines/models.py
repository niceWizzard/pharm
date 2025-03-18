import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class UnitType(models.TextChoices):
    ML = "ml", "Milliliters"
    EACH = "Each", "Each"
    PACK = "Pack", "Pack"
    G = "g", "Grams"
    PACKS = "Packs", "Packs"
    ROLLS = "Rolls", "Rolls"
    TUBES = "Tubes", "Tubes"
    BOTTLES = "Bottles", "Bottles"
    BARS = "Bars", "Bars"
    KITS = "Kits", "Kits"
    TABLETS = "Tablets", "Tablets"
    UNITS = "Units", "Units"
    CAPSULES = "Capsules", "Capsules"
    VIALS = "Vials", "Vials"
    SOFTGELS = "Softgels", "Softgels"
    TABLET = "Tablet", "Tablet"  # Singular form

# Create your models here.
class InventoryItem(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=128)
    category = models.CharField(max_length=32)
    subcategory = models.CharField(max_length=32)
    item_name = models.CharField(max_length=128)
    brand_name = models.CharField(max_length=128)
    generic_name = models.CharField(max_length=128)
    dosage_form = models.CharField(max_length=32)
    strength_per_size = models.CharField(max_length=32, null=True, default=None)
    packaging = models.CharField(max_length=32)
    quantity = models.IntegerField()
    unit_size = models.CharField(
        max_length=16,
        choices=UnitType.choices,
        default=UnitType.EACH,
    )
    date_of_delivery = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    stocks = models.PositiveIntegerField()


class InventoryTransaction(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transaction_type = models.CharField(
            max_length=10, choices=[("add", "Add"), ("remove", "Remove")]
        )  # Explicitly track addition or removal

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk:
            # Get the existing transaction before updating
            old_transaction = InventoryTransaction.objects.get(pk=self.pk)

            # Reverse previous transaction effect
            if old_transaction.transaction_type == "add":
                self.item.stocks -= old_transaction.quantity
            else:  # "remove" case
                self.item.stocks += old_transaction.quantity

        # Apply new transaction effect
        if self.transaction_type == "add":
            self.item.stocks += self.quantity
        else:  # "remove" case
            if self.item.stocks < self.quantity:
                raise ValueError("Not enough stock available")
            self.item.stocks -= self.quantity

        self.item.save()
        super().save(*args, **kwargs)
    
    @transaction.atomic
    def delete(self, *args, **kwargs):
        """Revert stock changes when transaction is deleted."""
        if self.transaction_type == "add":
            self.item.stocks -= self.quantity  # Remove added stock
        else:  # "remove" case
            self.item.stocks += self.quantity  # Restore removed stock

        self.item.save()  # Update stock in database
        super().delete(*args, **kwargs)