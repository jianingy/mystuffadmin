from django.conf import settings
from django.http import HttpResponse
from domain.models import DynamicDomainName
from domain.utils import ddns_update
from hashlib import md5
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
import time


def error(m):
    return HttpResponse("ERROR: %s" % m)


def update_ddns_ip(request):

    domain      = request.GET.get('domain', None)
    record_a    = request.GET.get('ipv4', '')
    record_aaaa = request.GET.get('ipv6', '')
    sig         = request.GET.get('sig', None)
    psk         = request.GET.get('psk', None)

    if not domain:
        return error("domain is missing.")

    if not record_a and not record_aaaa:
        ip = request.META['REMOTE_ADDR']
        if ip.find(':') > -1:
            record_aaaa = ip
        else:
            record_a = ip

    base_q = DynamicDomainName.objects.filter(fqdn="%s." % domain)

    try:
        entry = base_q.get()
        if entry.auth_mode == 1:
            if not sig:
                return error("signature is missing.")
            checkstr = ("%s.%s.%s.%s" %
                        (domain, record_a, record_aaaa, entry.psk))
            checksum = md5(checkstr).hexdigest()
            if sig != checksum:
                return error("signature is incorrect.")
        elif entry.psk != psk:
            return error("psk is incorrect.")
    except ObjectDoesNotExist:
        return error("domain does not exist.")
    except MultipleObjectsReturned:
        return error("mutiple domainname found. database is corrupted.")

    entry.record_a = record_a
    entry.record_aaaa = record_aaaa
    entry.save()

    ddns_update(entry)

    return HttpResponse("OK")


@login_required
def dig(request, pk):
    from subprocess import Popen, PIPE
    try:
        dynhost = DynamicDomainName.objects.get(pk=pk)

        result = Popen([settings.BIN_PATH["dig"],
                        "@127.0.0.1",
                        "%s.%s." % (dynhost.host, dynhost.domain),
                        "ANY"], stdout=PIPE).communicate()[0]
    except Exception as e:
        result = e

    return HttpResponse(result)
