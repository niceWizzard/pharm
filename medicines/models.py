import datetime
import uuid
import django
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

class PackagingType(models.TextChoices):
    BOTTLE = "bottle", "Bottle"
    BLISTER_PACK = "blister_pack", "Blister Pack"
    BOX = "box", "Box"
    PACK = "pack", "Pack"
    ROLL = "roll", "Roll"
    TUBE = "tube", "Tube"
    BAR = "bar", "Bar"
    ONE_BOX = "1_box", "1 box"
    HUNDRED_PER_PACK = "100_per_pack", "100's per pack"
    ONE_ROLL = "1_roll", "1 roll"
    ONE_TUBE = "1_tube", "1 tube"
    ONE_BOTTLE = "1_bottle", "1 bottle"
    ONE_BAR = "1_bar", "1 bar"
    ONE_KIT = "1_kit", "1 kit"
    TWENTY_PER_BOTTLE = "20_per_bottle", "20's per bottle"
    HUNDRED_ML_BOTTLE = "100ml_bottle", "100mL bottle"
    TEN_PER_BLISTER = "10_per_blister", "10's per blister"
    ONE_UNIT = "1_unit", "1 unit"
    SIX_PER_BLISTER = "6_per_blister", "6's per blister"
    TEN_ML_VIAL = "10ml_vial", "10mL vial"
    JAR = "jar", "Jar"
    THIRTY_PER_BOTTLE = "30_per_bottle", "30's per bottle"
    SIXTY_PER_BOTTLE = "60_per_bottle", "60's per bottle"

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
    packaging = models.CharField(
        max_length=32, 
        choices=PackagingType.choices
    )
    quantity = models.IntegerField()
    unit_size = models.CharField(
        max_length=16,
        choices=UnitType.choices,
        default=UnitType.EACH,
    )

    def clean(self):
        if self.unit_size not in UnitType.values:
            raise ValidationError(f"Invalid unit type: {self.unit_size}")
        if self.category not in CategoryType.values:
            raise ValidationError(f"Invalid Category type: {self.category}")
        if self.subcategory not in SubcategoryType.values:
            raise ValidationError(f"Invalid Subcategory type: {self.subcategory}")
        if self.packaging not in PackagingType.values:
            raise ValidationError(f"Invalid Packaging type: {self.packaging}")
    def save(self, *args, **kwargs):
        self.clean()  # Call validation before saving
        super().save(*args, **kwargs)

class InventoryStock(models.Model):
    id=models.AutoField(primary_key=True)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    date_of_delivery = models.DateField(default=django.utils.timezone.now)
    expiration_date = models.DateField(default=django.utils.timezone.now)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("item", "expiration_date")  # Prevent duplicate stock entries with the same expiration date.

    def clean(self):
        """Validation before saving."""
        if not self.pk and self.expiration_date < datetime.date.today():
            raise ValidationError("Cannot add stock with an expiration date in the past.")

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.clean()  # Ensure validations run before saving
        super().save(*args, **kwargs)

class InventoryTransaction(models.Model):
    ADD = "add"
    REMOVE = "remove"
    item_stock = models.ForeignKey(InventoryStock, on_delete=models.CASCADE)
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
                    self.item_stock.count -= old_transaction.quantity
                case self.REMOVE:
                    self.item_stock.count += old_transaction.quantity
                case _:
                    raise ValueError(f"Invalid transaction type: {self.transaction_type}")

        # Apply new transaction effect
        match self.transaction_type:
            case self.ADD:
                self.item_stock.count += self.quantity
            case self.REMOVE:
                if self.item_stock.count < self.quantity:
                    raise ValueError("Not enough stock available")
                self.item_stock.count -= self.quantity
            case _:
                raise ValueError(f"Invalid transaction type: {self.transaction_type}")

        self.item_stock.save()
        super().save(*args, **kwargs)
    
    @transaction.atomic
    def delete(self, *args, **kwargs):
        """Revert stock changes when transaction is deleted."""
        match self.transaction_type:
            case self.ADD:
                self.item_stock.count -= self.quantity  # Remove added stock
            case self.REMOVE:
                self.item_stock.count += self.quantity  # Restore removed stock
            case _:
                raise ValueError(f"Invalid transaction type: {self.transaction_type}")


        self.item_stock.save()  # Update stock in database
        super().delete(*args, **kwargs)