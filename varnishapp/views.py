from django.http import HttpResponseRedirect
from manager import manager
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings
from django.views.generic import TemplateView

def get_stats():
    stats = [x[0] for x in manager.run('stats', secret=getattr(settings, 'VARNISH_SECRET', None))]
    return zip(getattr(settings, 'VARNISH_MANAGEMENT_ADDRS', ()), stats)
    
def management(request): 
    if not request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    if 'command' in request.REQUEST:
        kwargs = dict(request.REQUEST.items())
        kwargs['secret'] = getattr(settings, 'VARNISH_SECRET', None)
        manager.run(*str(kwargs.pop('command')).split(), **kwargs)
        return HttpResponseRedirect(request.path)
    try:
        stats = get_stats()
        errors = {}
    except:
        stats = None
        errors = {"stats":"Impossible to access the stats for server : %s" \
                  %getattr(settings, 'VARNISH_MANAGEMENT_ADDRS', ())}
        
    extra_context = {'stats':stats,
                     'errors':errors}
    return render(request,
                  'varnish/report.html',
                  extra_context,
                  current_app='varnishapp',
                 )

    #return direct_to_template(request, template='varnish/report.html',
    #                          extra_context=extra_context)
