from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:category_products', args=[self.slug])
        
    def __str__(self):
        return self.name
        
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d')

    available = models.BooleanField(default=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def __str__(self):
        return self.name + self.category.name

