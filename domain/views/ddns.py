from django.shortcuts import redirect
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django_tables2 import SingleTableView
from django import forms

from domain.tables import DynamicDomainNameTable
from domain.models import DynamicDomainName
from domain.utils import ddns_update


class DynamicDomainNameForm(forms.ModelForm):

    domainname  = forms.CharField(label='domainname')
    psk         = forms.CharField(label='preshared key')

    record_a    = forms.GenericIPAddressField(label='ipv4 address',
                                              protocol='IPv4',
                                              required=False)
    record_aaaa = forms.GenericIPAddressField(label='ipv6 address',
                                              protocol='IPv6',
                                              required=False)

    def __init__(self, *args, **kwargs):
        super(DynamicDomainNameForm, self).__init__(*args, **kwargs)
        self.fields['zone'].label = "zone"
        self.fields['auth_mode'].label = "auth mode"

    class Meta:
        model = DynamicDomainName
        fields = ('domainname', 'zone',
                  'record_a', 'record_aaaa',
                  'psk', 'auth_mode')


class DynamicDomainNameTableView(SingleTableView):
    model = DynamicDomainName
    table_class = DynamicDomainNameTable
    template_name = 'dns/ddns/list.html'

    def get_queryset(self):
        base_q = DynamicDomainName.objects.filter(created_by=self.request.user)
        return base_q.order_by('id')


class DynamicDomainNameCreateView(CreateView):

    form_class = DynamicDomainNameForm
    model = DynamicDomainName
    template_name = 'dns/ddns/form.html'

    def get_context_data(self, **kwargs):
        context = super(DynamicDomainNameCreateView, self).get_context_data(**kwargs)
        context['form_action'] = 'create'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        ddns_update(self.object)
        return redirect('domain.views.ddns.list_view')


class DynamicDomainNameUpdateView(UpdateView):

    form_class = DynamicDomainNameForm
    model = DynamicDomainName
    template_name = 'dns/ddns/form.html'

    def get_context_data(self, **kwargs):
        context = super(DynamicDomainNameUpdateView, self).get_context_data(**kwargs)
        context['form_action'] = 'edit'
        context['record'] = self.object
        return context

    def get_success_url(self):
        return reverse_lazy('domain.views.ddns.list_view')

    def get_queryset(self):
        base_qs = super(DynamicDomainNameUpdateView, self).get_queryset()
        return base_qs.filter(created_by=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        ddns_update(self.object)
        return redirect(self.get_success_url())


class DynamicDomainNameDeleteView(DeleteView):

    model = DynamicDomainName
    success_url = reverse_lazy('domain.views.ddns.list_view')
    template_name = 'dns/ddns/confirm_delete.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DynamicDomainNameDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class DynamicDomainNameDocView(TemplateView):
    template_name = 'dns/ddns/doc.html'

doc_view = login_required(DynamicDomainNameDocView.as_view())
list_view = login_required(DynamicDomainNameTableView.as_view())
create_view = login_required(DynamicDomainNameCreateView.as_view())
update_view = login_required(DynamicDomainNameUpdateView.as_view())
delete_view = login_required(DynamicDomainNameDeleteView.as_view())
