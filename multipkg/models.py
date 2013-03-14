from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

VCS_SUBVERSION = 0
VCS_GIT = 1
VCS_MERCURIAL = 2

VCS_TYPE = (
    (VCS_SUBVERSION, 'Subversion'),
    (VCS_GIT, 'Git'),
    (VCS_MERCURIAL, 'Mercurial'),
)

VCS_TYPE_STRING = ('Subversion', 'Git', 'Mercurial')


class Package(models.Model):
    name           = models.CharField(_('name'), max_length=255,
                                     unique=True, db_index=True)
    version        = models.CharField(_('version'), max_length=255)
    release        = models.CharField(_('release'), max_length=255)
    build          = models.CharField(_('build'), max_length=255)
    summary        = models.TextField(_('summary'), null=True, blank=True)
    vcs_type       = models.IntegerField(_('VCS type'),
                                        choices=VCS_TYPE,
                                        default=0)
    vcs_address    = models.CharField(_('VCS address'), max_length=512)
    owner          = models.ForeignKey(User)
    quality        = models.IntegerField(_('Quality'))
    update_key     = models.CharField(_('update_key'), max_length=32)
    auto_update    = models.BooleanField(_('auto update'))

    recent_changes = models.TextField(_('recent changes'))

    def __unicode__(self):
        return "%s %s(%s.%s)" % (self.name, self.version,
                                 self.release, self.build)

    class Meta:
        verbose_name = _('package')
        verbose_name_plural = verbose_name
