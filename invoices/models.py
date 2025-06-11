from django.db import models

class Invoice(models.Model):
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    service_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.client_name}"
