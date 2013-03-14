# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django_tables2 import SingleTableView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from multipkg.forms import PackageCreateForm
from multipkg.tables import PackageTable
from multipkg.models import Package


class FileFormatError(Exception):
    pass


class PackageNameInconsistentError(Exception):
    pass


class PackageTableView(SingleTableView):
    model = Package
    table_class = PackageTable
    template_name = 'multipkg/list.html'

    def get_queryset(self):
        base_q = self.model.objects
        return base_q.order_by('id')


class PackageDetailView(DetailView):
    model = Package
    template_name = 'multipkg/detail.html'


class PackageCreateView(CreateView):
    form_class = PackageCreateForm
    template_name = 'multipkg/create.html'
    success_url = reverse_lazy('multipkg/home')

    def get_initial(self):
        initial = super(PackageCreateView, self).get_initial()
        initial['user'] = self.request.user
        return initial


def sync_view(request, pk):
    from multipkg.models import VCS_SUBVERSION, VCS_MERCURIAL
    from multipkg.utils import get_yaml_from_subversion
    from multipkg.utils import get_yaml_from_mercurial
    from multipkg.forms import PackageCreateForm

    default_fields = PackageCreateForm.default_fields

    try:
        package = Package.objects.get(pk=pk)
        if package.vcs_type == VCS_SUBVERSION:
            yaml = get_yaml_from_subversion(package.vcs_address)
        elif package.vcs_type == VCS_MERCURIAL:
            yaml = get_yaml_from_mercurial(package.vcs_address)

        default = yaml['default']
        map(lambda x: yaml['default'].setdefault(x, ''), default_fields)

        if package.name != default['name']:
            raise PackageNameInconsistentError()

        package.name = default['name']
        package.version = default['version']
        package.build = default['build']
        package.release = default['release']
        package.summary = default['summary']

        package.recent_changes = yaml['.']['recent_changes']

        package.save()
        return HttpResponse('OK')
    except Package.DoesNotExist:
        return HttpResponse('NOTEXIST')

list_view = PackageTableView.as_view()
detail_view = PackageDetailView.as_view()
create_view = login_required(PackageCreateView.as_view())
