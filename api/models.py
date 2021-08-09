from django.contrib.gis.db import models


class District(models.Model):
    name = models.CharField(max_length=18)
    district_code = models.CharField(max_length=9, unique=True)

    def __repr__(self):
        return "District <id=%s, name=%s>" % (self.id, self.name)

    class Meta:
        ordering = ["-id"]
        indexes = [models.Index(fields=["name"], name="district_name_idx")]


class SubCityHall(models.Model):
    name = models.CharField(max_length=25)
    cod_sub_city_hall = models.CharField(max_length=2, unique=True)

    def __repr__(self):
        return "SubCityHall <id=%s, name=%s>" % (self.id, self.name)

    class Meta:
        ordering = ["-id"]


class Region(models.Model):
    name = models.CharField(max_length=6, unique=True)

    def __repr__(self):
        return "Region <id=%s, name=%s>" % (self.id, self.name)

    class Meta:
        ordering = ["-id"]
        indexes = [models.Index(fields=["name"], name="region_name_idx")]


class SubRegion(models.Model):
    name = models.CharField(max_length=7)
    region = models.ForeignKey(
        Region, related_name="sub_regions", on_delete=models.CASCADE
    )

    def __repr__(self):
        return "SubRegion <id=%s, name=%s>" % (self.id, self.name)

    class Meta:
        ordering = ["id"]
        unique_together = ("name", "region")


class Neighborhood(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __repr__(self):
        return "Neighborhood <id=%s, name=%s>" % (self.id, self.name)

    class Meta:
        ordering = ["-id"]
        indexes = [models.Index(fields=["name"], name="neighborhood_name_idx")]


class OpenMarket(models.Model):
    name = models.CharField(max_length=30)
    register = models.CharField(max_length=6, unique=True)
    location = models.PointField()
    sector = models.CharField(max_length=15)
    area = models.CharField(max_length=13)
    public_place = models.CharField(max_length=34)
    number = models.CharField(max_length=5, default="", blank=True)
    ref = models.CharField(max_length=24)

    district = models.ForeignKey(
        District, related_name="open_markets", on_delete=models.CASCADE
    )
    sub_city_hall = models.ForeignKey(
        SubCityHall, related_name="open_markets", on_delete=models.CASCADE
    )
    sub_region = models.ForeignKey(
        SubRegion, related_name="open_markets", on_delete=models.CASCADE
    )
    neighborhood = models.ForeignKey(
        Neighborhood, related_name="neighborhood", on_delete=models.CASCADE
    )

    def __repr__(self):
        return "Open Market <id=%s, register=%s>" % (self.id, self.register)

    class Meta:
        ordering = ["-id"]
        indexes = [models.Index(fields=["name"], name="open_market_name_idx")]
