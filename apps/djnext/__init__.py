from django.http import HttpResponseRedirect

# Ask GET then POST
def get_post(request, url, key="next"):
    return request.GET.get(key, request.POST.get(key, url))

def get_post_response(*args, **kwargs):
    return HttpResponseRedirect(get_post(*args, **kwargs))

# Ask POST then GET
def post_get(request, url, key="next"):
    return request.POST.get(key, request.GET.get(key, url))

def post_get_response(*args, **kwargs):
    return HttpResponseRedirect(post_get(*args, **kwargs))

# REFERRER ?
def ref_get_post(request, url, key="next"):
    return request.META.get("HTTP_REFERER", request.GET.get(key, request.POST.get(key, url)))