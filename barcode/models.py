from django.db import models

class Certificate(models.Model):
    title = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255)
    certificate_number = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    issue_date = models.DateField()
    image = models.ImageField(upload_to="certificate", default="")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.certificate_number}"
    
    def save(self, *args, **kwargs):
        # Ensure the name is saved in title case
        self.name = self.name.title() if self.name else self.name  # Handle empty names gracefully
        super(Certificate, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Certificates"

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email