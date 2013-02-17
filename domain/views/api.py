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

    domainname  = request.GET.get('domainname', None)
    zone        = request.GET.get('zone', None)
    record_a    = request.GET.get('ipv4', '')
    record_aaaa = request.GET.get('ipv6', '')
    sig         = request.GET.get('sig', None)
    psk         = request.GET.get('psk', None)

    if not domainname or not zone:
        return error("domainname or zone is missing.")

    if not record_a and not record_aaaa:
        ip = request.META['REMOTE_ADDR']
        if ip.find(':') > -1:
            record_aaaa = ip
        else:
            record_a = ip

    base_q = DynamicDomainName.objects.filter(domainname=domainname)
    base_q = base_q.filter(zone__name=zone)

    try:
        entry = base_q.get()
        if entry.require_signature:
            if not sig:
                return error("signature is missing.")
            checkstr = ("%s.%s.%s.%s.%s" %
                        (domainname, zone, record_a, record_aaaa, entry.psk))
            checksum = md5(checkstr).hexdigest()
            if sig != checksum:
                return error("signature is incorrect.")
        elif entry.psk != psk:
            return error("psk is incorrect.")
    except ObjectDoesNotExist:
        return error("domainname does not exist.")
    except MultipleObjectsReturned:
        return error("mutiple domainname found. database is corrupted.")

    entry.record_a = record_a
    entry.record_aaaa = record_aaaa
    entry.save()

    ddns_update(entry)

    return HttpResponse("Request Queued")


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
