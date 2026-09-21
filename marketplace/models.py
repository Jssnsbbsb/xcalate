import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.text import slugify


def validate_images(value):
	if not isinstance(value, list):
		raise ValidationError("Images must be a list of URLs.")

	if len(value) > 10:
		raise ValidationError("A listing can have at most 10 images.")

	url_validator = URLValidator()
	for image_url in value:
		url_validator(image_url)


class Listing(models.Model):
	TYPE_CHOICES = [
		("product", "Product"),
		("service", "Service"),
	]

	REGION_CHOICES = [
		("imphal", "Imphal"),
		("loktak", "Loktak"),
		("ukhrul", "Ukhrul"),
		("churachandpur", "Churachandpur"),
		("senapati", "Senapati"),
		("tamenglong", "Tamenglong"),
		("bishnupur", "Bishnupur"),
		("thoubal", "Thoubal"),
	]

	PRODUCT_CATEGORY_CHOICES = [
		("handicraft", "Handicraft"),
		("textile", "Textile"),
		("food", "Food"),
		("art", "Art"),
		("jewelry", "Jewelry"),
		("other", "Other"),
	]
	SERVICE_CATEGORY_CHOICES = [
		("guide", "Guide"),
		("workshop", "Workshop"),
		("transport", "Transport"),
		("performance", "Performance"),
		("other", "Other"),
	]
	CATEGORY_CHOICES = [
		*PRODUCT_CATEGORY_CHOICES[:-1],
		*SERVICE_CATEGORY_CHOICES[:-1],
		("other", "Other"),
	]

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="marketplace_listings",
		limit_choices_to={"role": "local"},
	)
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True, blank=True)
	description = models.TextField()
	short_description = models.CharField(max_length=280)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	price_unit = models.CharField(max_length=30)
	images = models.JSONField(default=list, blank=True, validators=[validate_images])
	region = models.CharField(max_length=20, choices=REGION_CHOICES)
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
	contact_phone = models.CharField(max_length=40)
	contact_email = models.EmailField(blank=True)
	whatsapp = models.CharField(max_length=40, blank=True)
	is_active = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=False)
	view_count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-is_featured", "-created_at"]
		indexes = [
			models.Index(fields=["type"]),
			models.Index(fields=["region"]),
			models.Index(fields=["category"]),
		]

	def clean(self):
		super().clean()
		if self.user_id and self.user.role != "local":
			raise ValidationError({"user": "Only local users can create listings."})

		product_categories = {value for value, label in self.PRODUCT_CATEGORY_CHOICES}
		service_categories = {value for value, label in self.SERVICE_CATEGORY_CHOICES}
		if self.type == "product" and self.category not in product_categories:
			raise ValidationError({"category": "Products must use a product category."})
		if self.type == "service" and self.category not in service_categories:
			raise ValidationError({"category": "Services must use a service category."})

	def save(self, *args, **kwargs):
		if not self.slug:
			base = slugify(self.title)[:210] or "listing"
			self.slug = f"{base}-{uuid.uuid4().hex[:8]}"
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title


class ContactRequest(models.Model):
	listing = models.ForeignKey(
		Listing,
		on_delete=models.CASCADE,
		related_name="contacts",
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="contact_requests",
	)
	name = models.CharField(max_length=120)
	phone = models.CharField(max_length=40)
	email = models.EmailField(blank=True)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Contact request from {self.name} for {self.listing.title}"
