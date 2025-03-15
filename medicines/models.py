import uuid
from django.db import models
from django.contrib.auth import get_user_model

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

    def save(self, *args, **kwargs):
        # Check if it's a new transaction
        if not self.pk:
            if self.transaction_type == "remove":
                if self.item.stocks < self.quantity:
                    raise ValueError("Not enough stock available")
                self.item.stocks -= self.quantity
            else:  # "add" case
                self.item.stocks += self.quantity
            
            self.item.save()  # Save updated stocks

        super().save(*args, **kwargs)