from django.db import models

from apps.organization.utils import generate_random_string


# Create your models here.


class Organization(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='organizations', default=1,
                             blank=True, null=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # additional fields
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # profile image
    organization_image_save_path = 'organization_images/%Y/%m/%d/' + generate_random_string()
    organization_image = models.ImageField(upload_to=organization_image_save_path, blank=True, max_length=1000,
                                           null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ["-created_at"]



