from django.db import models


class State(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)


class County(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)


class Commodity(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)


class OperationType(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)


class DevelopmentStatus(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)


class WorkType(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)


class Site(models.Model):
    COMMODITY_TYPE_CHOICES = {
        ('', '----------'),
        ('M', 'Metallic'),
        ('N', 'Non-metallic'),
        ('B', 'Both')
    }

    dep_id = models.CharField(max_length=255, default='', blank=True)
    mrds_url = models.URLField(max_length=255, default='', blank=True)
    mrds_id = models.CharField(max_length=255, default='', blank=True)
    mas_id = models.CharField(max_length=255, default='', blank=True)
    site_name = models.CharField(max_length=255, default='', blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    region = models.CharField(max_length=255, default='', blank=True)
    country = models.CharField(max_length=255, default='', blank=True)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    com_type = models.CharField(max_length=255, default='', blank=True, choices=COMMODITY_TYPE_CHOICES)
    commodity_1 = models.ForeignKey(
        Commodity, null=True, blank=True, on_delete=models.SET_NULL, related_name='primary_sites')
    commodity_2 = models.ForeignKey(
        Commodity, null=True, blank=True, on_delete=models.SET_NULL, related_name='secondary_sites')
    commodity_3 = models.ForeignKey(
        Commodity, null=True, blank=True, on_delete=models.SET_NULL, related_name='tertiary_sites')
    operation_type = models.ForeignKey(OperationType, null=True, blank=True, on_delete=models.SET_NULL)
    dep_type = models.CharField(max_length=255, default='', blank=True)
    prod_size = models.CharField(max_length=50, default='', blank=True)
    development_status = models.ForeignKey(DevelopmentStatus, null=True, blank=True, on_delete=models.SET_NULL)
    ore = models.TextField(default='', blank=True)
    gangue = models.TextField(default='', blank=True)  # Non-economic minerals of the deposit
    other_matl = models.TextField(default='', blank=True)
    orebody_fm = models.TextField(default='', blank=True)
    geo_model = models.TextField(default='', blank=True, verbose_name='Model')
    alteration = models.TextField(default='', blank=True)
    conc_proc = models.TextField(default='', blank=True)
    alt_previous_names = models.TextField(default='', blank=True)
    ore_control = models.TextField(default='', blank=True)
    reporter = models.TextField(default='', blank=True)
    hrock_unit = models.TextField(default='', blank=True)
    hrock_type = models.TextField(default='', blank=True)
    arock_unit = models.TextField(default='', blank=True)
    arock_type = models.TextField(default='', blank=True)
    structure = models.TextField(default='', blank=True)
    tectonic = models.TextField(default='', blank=True)
    ref = models.TextField(default='', blank=True)
    yfp_ba = models.TextField(default='', blank=True)
    yr_fst_prd = models.TextField(default='', blank=True)
    ylp_ba = models.TextField(default='', blank=True)
    yr_lst_prd = models.TextField(default='', blank=True)
    dy_ba = models.TextField(default='', blank=True)
    disc_yr = models.TextField(default='', blank=True)
    prod_yrs = models.TextField(default='', blank=True)
    discr = models.TextField(default='', blank=True)








