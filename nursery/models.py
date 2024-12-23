import contextlib
from django.db import models
from PIL import Image
from datetime import datetime
from django.templatetags.static import static


class Satvai(models.Model):
    plant_name = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(
        upload_to="satvai",
        max_length=255,
        # validators=[validate_file_extension],
        # default="ContractorsImage/default.png",
        null=True,
        blank=True,
    )

    @property
    def plant_image(self):
        try:
            plant_image = self.image.url
        except Exception:
            plant_image = static('images/1f331.svg')
        return plant_image
    def __str__(self):
        return f"{self.plant_name}, {self.category}"
        

class Brihat(models.Model):
    product_name = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(
        upload_to="brihat",
        max_length=255,
        # validators=[validate_file_extension],
        # default="ContractorsImage/default.png",
        null=True,
        blank=True,
    )
    @property
    def plant_image(self):
        try:
            plant_image = self.image.url
        except Exception:
            plant_image = static('images/1f33c.svg')
        return plant_image
    
    def __str__(self):
        return f"{self.product_name}, {self.title}"

class CPVP(models.Model):
    praktony_name = models.CharField(max_length=200, blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField("Email", max_length=300, blank=True, null=True)
    reg_date = models.DateField(default=datetime.now)
    image = models.ImageField(
        upload_to="cpvp",
        max_length=255,
        null=True,
        blank=True,
    )

    def save(self):
        super().save()
        with contextlib.suppress(Exception):
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                new_image_height = int(300*(img.size[1]/300))
                output_size = (300,new_image_height)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return f"{self.praktony_name}, {self.batch}"