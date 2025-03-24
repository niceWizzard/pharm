import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db import transaction
from django.forms import ValidationError

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

class CategoryType(models.TextChoices):
    ANTACIDS = "Antacids", "Antacids"
    COUGH_AND_COLD = "Cough and Cold", "Cough and Cold"
    DIGESTIVE_HEALTH = "Digestive Health", "Digestive Health"
    EYE_CARE = "Eye Care", "Eye Care"
    MEDICAL_SUPPLIES = "Medical Supplies & Personal Care", "Medical Supplies & Personal Care"
    MEDICAL_SUPPLIES_ALT = "Medical Supplies and Personal Care Products", "Medical Supplies and Personal Care Products"
    OTC_MEDICINES = "Over-the-Counter (OTC) Medicines", "Over-the-Counter (OTC) Medicines"
    PAIN_RELIEVERS = "Pain Relievers", "Pain Relievers"
    PHARMACY_EQUIPMENT = "Pharmacy Machineries and Equipment", "Pharmacy Machineries and Equipment"
    PRESCRIPTION_MEDICINES = "Prescription Medicines", "Prescription Medicines"
    SKIN_CARE = "Skin Care", "Skin Care"
    TOPICAL_TREATMENTS = "Topical Treatments", "Topical Treatments"
    VITAMINS_SUPPLEMENTS = "Vitamins and Supplements", "Vitamins and Supplements"

class SubcategoryType(models.TextChoices):
    ANTACID = "Antacid", "Antacid"
    DECONGESTANTS = "Decongestants", "Decongestants"
    EXPECTORANTS = "Expectorants", "Expectorants"
    ANTIHISTAMINES = "Antihistamines", "Antihistamines"
    ANTITUSSIVES = "Antitussives", "Antitussives"
    LAXATIVES = "Laxatives", "Laxatives"
    LUBRICATING_DROPS = "Lubricating Drops", "Lubricating Drops"
    FIRST_AID_SUPPLIES = "First Aid Supplies", "First Aid Supplies"
    PERSONAL_HYGIENE = "Personal Hygiene", "Personal Hygiene"
    SKIN_CARE = "Skin Care", "Skin Care"
    INCONTINENCE_CARE = "Incontinence Care", "Incontinence Care"
    BABY_CARE = "Baby Care", "Baby Care"
    EYE_CARE = "Eye Care", "Eye Care"
    MEDICAL_SUPPLIES = "Medical Supplies", "Medical Supplies"
    BANDAGES_AND_DRESSINGS = "Bandages and Dressings", "Bandages and Dressings"
    FIRST_AID_KITS = "First Aid Kits", "First Aid Kits"
    PAIN_RELIEVERS = "Pain Relievers", "Pain Relievers"
    COUGH_AND_COLD_REMEDIES = "Cough and Cold Remedies", "Cough and Cold Remedies"
    ANALGESICS = "Analgesics", "Analgesics"
    BLOOD_PRESSURE_MONITORS = "Blood Pressure Monitors", "Blood Pressure Monitors"
    THERMOMETERS = "Thermometers", "Thermometers"
    NEBULIZERS = "Nebulizers", "Nebulizers"
    OXYGEN_EQUIPMENT = "Oxygen Equipment", "Oxygen Equipment"
    PULSE_OXIMETERS = "Pulse Oximeters", "Pulse Oximeters"
    SURGICAL_INSTRUMENTS = "Surgical Instruments", "Surgical Instruments"
    ANTIBIOTICS = "Antibiotics", "Antibiotics"
    ANTIHYPERTENSIVES = "Antihypertensives", "Antihypertensives"
    ANTI_DIABETIC_MEDICATIONS = "Anti-Diabetic Medications", "Anti-Diabetic Medications"
    SUNSCREEN = "Sunscreen", "Sunscreen"
    MOISTURIZER = "Moisturizer", "Moisturizer"
    ACNE_TREATMENT = "Acne Treatment", "Acne Treatment"
    ANTI_FUNGAL = "Anti-fungal", "Anti-fungal"
    ANTI_INFLAMMATORY = "Anti-inflammatory", "Anti-inflammatory"
    PAIN_RELIEF = "Pain Relief", "Pain Relief"
    MULTIVITAMINS = "Multivitamins", "Multivitamins"
    VITAMIN_C = "Vitamin C", "Vitamin C"
    OMEGA_3_FATTY_ACIDS = "Omega-3 Fatty Acids", "Omega-3 Fatty Acids"
    IRON_SUPPLEMENTS = "Iron Supplements", "Iron Supplements"
    VITAMIN_D = "Vitamin D", "Vitamin D"
    VITAMIN_B_COMPLEX = "Vitamin B Complex", "Vitamin B Complex"
    VITAMIN_E = "Vitamin E", "Vitamin E"
    CALCIUM = "Calcium", "Calcium"
    IRON = "Iron", "Iron"
    OMEGA_3 = "Omega-3", "Omega-3"
    PROBIOTICS = "Probiotics", "Probiotics"
    HERBAL_SUPPLEMENTS = "Herbal Supplements", "Herbal Supplements"
    JOINT_HEALTH = "Joint Health", "Joint Health"
    ENERGY_ENDURANCE = "Energy & Endurance", "Energy & Endurance"

# Create your models here.
class InventoryItem(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=128)
    category = models.CharField(
        max_length=64,
        choices=CategoryType.choices,
        default=CategoryType.OTC_MEDICINES,
    )
    subcategory = models.CharField(
        max_length=64,
        choices=SubcategoryType.choices,
    )
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
    stocks = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.unit_size not in UnitType.values:
            raise ValidationError(f"Invalid unit type: {self.unit_size}")
    def save(self, *args, **kwargs):
        self.clean()  # Call validation before saving
        super().save(*args, **kwargs)


class InventoryTransaction(models.Model):
    ADD = "add"
    REMOVE = "remove"
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transaction_type = models.CharField(
            max_length=10, choices=[(ADD, "Add"), (REMOVE, "Remove")]
        )  # Explicitly track addition or removal

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk:
            # Get the existing transaction before updating
            old_transaction = InventoryTransaction.objects.get(pk=self.pk)

            # Reverse previous transaction effect
            match old_transaction.transaction_type:
                case self.ADD:
                    self.item.stocks -= old_transaction.quantity
                case self.REMOVE:
                    self.item.stocks += old_transaction.quantity
                case _:
                    raise ValueError(f"Invalid transaction type: {self.transaction_type}")

        # Apply new transaction effect
        match self.transaction_type:
            case self.ADD:
                self.item.stocks += self.quantity
            case self.REMOVE:
                if self.item.stocks < self.quantity:
                    raise ValueError("Not enough stock available")
                self.item.stocks -= self.quantity
            case _:
                raise ValueError(f"Invalid transaction type: {self.transaction_type}")

        self.item.save()
        super().save(*args, **kwargs)
    
    @transaction.atomic
    def delete(self, *args, **kwargs):
        """Revert stock changes when transaction is deleted."""
        match self.transaction_type:
            case self.ADD:
                self.item.stocks -= self.quantity  # Remove added stock
            case self.REMOVE:
                self.item.stocks += self.quantity  # Restore removed stock
            case _:
                raise ValueError(f"Invalid transaction type: {self.transaction_type}")


        self.item.save()  # Update stock in database
        super().delete(*args, **kwargs)