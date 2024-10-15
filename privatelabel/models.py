from django.db import models
from django.utils import timezone

# Create your models here.
#  customer model
class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# product model with name only
class Product(models.Model):
    sku = models.CharField(max_length=200, unique=True, null=True, blank=True)
    spec_version = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, blank=True, related_name='products')
    package = models.CharField(
        max_length=20,
        choices=[
            ('Bottle', 'Bottle'),
            ('Tube', 'Tube'),
            ('Pump', 'Pump'),
            ('Jar', 'Jar'),
            ('Sachet', 'Sachet'),
        ],
        default='Bottle'
    )
    cap = models.CharField(
        max_length=20,
        choices=[
            ('Flip Top', 'Flip Top'),
            ('Disc Cap', 'Disc Cap'),
            ('Pump', 'Pump'),
            ('Screw Cap', 'Screw Cap'),
            ('Spray', 'Spray'),
            ('Twist Cap', 'Twist Cap'),
            ('None', 'None'),
            ('N/A', 'N/A'),
        ],
        default='Flip Top'
    )
    label = models.CharField(
        max_length=20,
        choices=[
            ('Customer Supplied', 'Customer Supplied'),
            ('Custom Label', 'Custom Label'),
            ('None', 'None')
        ],
        default='Customer Supplied'
    )
    lube = models.CharField(
        max_length=20,
        choices=[
            ('Glide', 'Glide'),
            ('Silk', 'Silk'),
            ('Millennium', 'Millennium'),
            ('Free', 'Free'),
        ],
        default='Glide'
    )
    size = models.CharField(
        max_length=20,
        choices=[
            ('12 ml', '12 ml'),
            ('1 oz', '1 oz'),
            ('2.2 oz', '2.2 oz'),
            ('4.4 oz', '4.4 oz'),
            ('8 oz', '8 oz'),
            ('16 oz', '16 oz'),
            ('32 oz', '32 oz'),
            ('64 oz', '64 oz'),
            ('128 oz', '128 oz'),
        ],
        default='12 ml'
    )

    def __str__(self):
        return self.name

# order model
class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    number = models.CharField(max_length=200)
    qty = models.IntegerField(blank=True, null=True)
    date_received = models.DateField(blank=True, null=True)
    date_entered = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    desired_date = models.DateField(blank=True, null=True)
    expected_ship_date = models.DateField(blank=True, null=True)
    # week_scheduled = models.IntegerField(blank=True, null=True)
    deposit_stat = models.BooleanField(default=False)
    ingredients_stat = models.BooleanField(default=False)
    spec_stat = models.BooleanField(default=False)
    package_stat = models.BooleanField(default=False)
    cap_stat = models.BooleanField(default=False)
    label_stat = models.BooleanField(default=False)
    box_stat = models.BooleanField(default=False)
    last_component_eta = models.DateField(blank=True, null=True)
    released_to_warehouse = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    coordinator_notes = models.TextField(blank=True, null=True)
    planning_notes = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Deposit', 'Deposit'),
            ('Ingredients', 'Ingredients'),
            ('Spec', 'Spec'),
            ('Package', 'Package'),
            ('Cap', 'Cap'),
            ('Label', 'Label'),
            ('Box', 'Box'),
            ('Schedule', 'Schedule'),
            ('Ship', 'Ship'),
        ],
        default='Deposit'
    )

    def __str__(self):
        return self.product.name

# note model
class Note(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name='notes')
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content