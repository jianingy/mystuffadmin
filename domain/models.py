from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

AUTH_MODE_CHOICES = (
    (0, 'PSK only'),
    (1, 'PSK with signature'),
    (2, 'Refuse dynamic update'),
)


class Zone(models.Model):
    name          = models.CharField(_('name'), max_length=255,
                                     unique=True, db_index=True)
    key           = models.CharField(_('key'), max_length=1023,
                                     blank=True, null=True)
    master_server = models.GenericIPAddressField(protocol='both',
                                                 verbose_name=
                                                 _('master server'))

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('zone')
        verbose_name_plural = verbose_name


class DynamicDomainName(models.Model):

    domainname  = models.CharField(_('domainname'), max_length=255,
                                   db_index=True)
    fqdn        = models.CharField(_('domainname'), max_length=255,
                                   db_index=True)
    zone        = models.ForeignKey(Zone, verbose_name=_('zone'))
    psk         = models.CharField(_('preshared key'), max_length=63,
                                   null=True, blank=True)
    last_update = models.DateTimeField(_('last update'), auto_now=True,
                                       blank=True, null=True)
    created_by  = models.ForeignKey(User)

    record_a    = models.GenericIPAddressField(verbose_name=_('ipv4 address'),
                                               protocol='IPv4',
                                               blank=True,
                                               null=True)

    record_aaaa = models.GenericIPAddressField(verbose_name=_('ipv6 address'),
                                               protocol='IPv6',
                                               blank=True,
                                               null=True)

    auth_mode = models.IntegerField(_('auth mode'), choices=AUTH_MODE_CHOICES,
                                    default=0, db_index=True)

    def __unicode__(self):
        return "%s.%s" % (self.domainname, self.zone.name)

    def isOwnedBy(self, user):
        return self.created_by == user

    def save(self, *args, **kwargs):
        self.fqdn = "%s.%s." % (self.domainname, self.zone.name)
        super(DynamicDomainName, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('dynamic domain name')
        verbose_name_plural = verbose_name
        unique_together = ('domainname', 'zone',)
