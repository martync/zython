from units import settings as app_settings

def user_units(request):
    resp = {}
    prefix = getattr(app_settings, 'CONTEXT_PREFIX', "unit_")
    for k,d in app_settings.UNITS.items():
        key = "%s%s" % (prefix,k)
        user_val = request.session.get(key)
        if not user_val:
            user_val = d['choices'][0][0]
        request.session[key]= user_val
        resp[key] = user_val
    return resp


def unit_menu(request):
    menu = []
    prefix = getattr(app_settings, 'CONTEXT_PREFIX', "unit_")
    for k,d in app_settings.UNITS.items():
        key = "%s%s" % (prefix,k)
        user_val = request.session.get(key)
        items = []
        for item in d.get('choices'):
            items.append({
                "key": item[0],
                "title": item[1],
                "is_active": item[0] == user_val
            })

        menu.append({
            "title": d.get('verbose_name'),
            "key": k,
            "items": items
        })
    return {"unit_menu": menu}