from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


class Brand(models.Model):
    id_brand = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, default='', null=False, blank=False)

    def __str__(self):
        return self.name

class Image(models.Model):
    id_image = models.AutoField(primary_key=True)
    image = CloudinaryField('image', folder='products/')

    def __str__(self):
        if self.image and hasattr(self.image, 'public_id'):
            # Extraer solo el nombre del archivo del public_id
            # El public_id incluye la carpeta, así que tomamos la última parte
            filename = self.image.public_id.split('/')[-1]
            return filename
        return f"Imagen {self.id_image}"
    

class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    ]

    id_product = models.AutoField(primary_key=True)    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False, blank=False)

    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='', null=False, blank=False)
    description = models.CharField(max_length=200, default='', null=False, blank=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    id_size = models.AutoField(primary_key=True)
    size = models.CharField(max_length=5, default='', null=False, blank=False)

    def __str__(self):
        return self.size


class Color(models.Model):
    id_color = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', null=False, blank=False)

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    id_product_detail = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)

    price = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=False, blank=False)
    stock = models.IntegerField(default=0, null=False, blank=False)
    
    # class Meta genera que no existan productos con el mismo id_product, id_size y id_color en la base de datos
    # esto es para que no se puedan crear productos con el mismo id_product, id_size y id_color en la base de datos
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'size', 'color'], name='unique_product_detail')
        ]   

    def __str__(self):
        return self.product.name if self.product else 'Producto sin nombre'

        