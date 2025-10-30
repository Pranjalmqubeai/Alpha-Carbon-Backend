from django.db import models

class Project(models.Model):
    id = models.SlugField(primary_key=True, max_length=120)  # e.g. "redd-brazil-nut"
    kind = models.CharField(max_length=80)  # "CARBON OFFSETTING"
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=120)
    country_flag = models.CharField(max_length=8, blank=True, null=True)  # "🇵🇪"
    price = models.DecimalField(max_digits=10, decimal_places=2)  # per tCO2e
    sdg_score = models.PositiveIntegerField(default=0)
    thumb = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # coords
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    # Info (flattened for simplicity)
    info_company = models.CharField(max_length=255, blank=True, null=True)
    info_address = models.CharField(max_length=512, blank=True, null=True)
    info_website = models.URLField(blank=True, null=True)
    info_blockchain = models.CharField(max_length=255, blank=True, null=True)
    info_type = models.CharField(max_length=255, blank=True, null=True)
    info_mechanism = models.CharField(max_length=255, blank=True, null=True)
    info_characteristics = models.CharField(max_length=255, blank=True, null=True)
    info_registry = models.CharField(max_length=255, blank=True, null=True)
    info_registry_url = models.URLField(blank=True, null=True)
    info_validator = models.CharField(max_length=255, blank=True, null=True)
    info_status = models.CharField(max_length=120, blank=True, null=True)
    info_credit_start = models.CharField(max_length=120, blank=True, null=True)
    info_credit_end = models.CharField(max_length=120, blank=True, null=True)

    # SDGs as simple comma string (or make a relation if you prefer)
    sdgs_csv = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    url = models.URLField()


class Impact(models.Model):
    project = models.ForeignKey(Project, related_name="impacts", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)


class Vintage(models.Model):
    project = models.ForeignKey(Project, related_name="vintages", on_delete=models.CASCADE)
    year = models.IntegerField()
    volume = models.BigIntegerField()          # tCO2e
    unit = models.CharField(max_length=32)     # "tCO2e"
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Document(models.Model):
    project = models.ForeignKey(Project, related_name="docs", on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    url = models.URLField()


class Transaction(models.Model):
    project = models.ForeignKey(Project, related_name="transactions", on_delete=models.CASCADE)
    country = models.CharField(max_length=8)  # "GB"
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    units = models.IntegerField()
    date = models.CharField(max_length=64)  # keep as string for now ("Oct 21, 2025")
