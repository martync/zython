

def float1(val):
    return "%.1f" % float(val)


def float2(val):
    return "%.2f" % float(val)


def lower_str(val):
    return val.lower()


def potential_gravity(val):
    return "%.4f" % float(val)


def correct_malt_type(val):
    try:
        return {
            'Dry Extract': 'dryextract',
            'Extract': 'extract',
            'Sugar': 'sugar',
            'Adjunct': 'adjunct',
            'Grain': 'grain',
        }[str(val)]
    except KeyError:
        return 'grain'


def hop_type(val):
    return val.lower()


def hop_form(val):
    return 'leaf'


def hop_usage(val):
    if 'DRY' in val.upper():
        return 'dryhop'
    return 'boil'


def flocculation(val):
    return{
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Very High': 4
    }[val]


FERMENTABLE_FIELDS = (
    ("NAME",     "name"),
    ("ORIGIN",   "origin"),
    ("TYPE",     "malt_type",    correct_malt_type),
    ("POTENTIAL",     "potential_gravity",    potential_gravity),
    ("YIELD", "malt_yield", float2),
    ("COLOR", "color", float1),
    ("DIASTATIC_POWER", "diastatic_power", float1),
    ("PROTEIN", "protein", float1),
    ("MAX_IN_BATCH", "max_in_batch", float1),
    ("NOTES", "notes")
)

HOP_FIELDS = (
    ("NAME",     "name"),
    ("ORIGIN",     "origin"),
    ("ALPHA",     "acid_alpha",     float2),
    ("BETA",     "acid_beta",       float2),
    ("USE",     "usage",       hop_usage),
    ("FORM",     "form",       hop_form),
    ("TYPE",     "hop_type",       hop_type),
    ("NOTES",     "notes"),
)

MISC_FIELDS = (
    ("NAME",     "name"),
    ("TYPE",     "misc_type",       lower_str),
    ("USE_FOR",     "usage"),
    ("USE",         "use_in",       lower_str),
    ("NOTES",     "notes"),
)

YEAST_FIELDS = (
    ("NAME",        "name"),
    ("LABORATORY",  "laboratory"),
    ("PRODUCT_ID",  "product_id"),
    ("TYPE",        "yeast_type",       lower_str),
    ("FORM",        "form",       lower_str),
    ("FLOCCULATION", "flocculation",       flocculation),
    ("ATTENUATION",  "min_attenuation"),
    ("ATTENUATION",  "max_attenuation"),
    ("MIN_TEMPERATURE",  "min_temperature"),
    ("MAX_TEMPERATURE",  "max_temperature"),
    ("BEST_FOR",  "best_for"),
    ("NOTES",  "notes")
)

STYLE_FIELDS = (
    ("NAME",     "name"),
    ("CATEGORY",     "category"),
    ("CATEGORY_NUMBER",     "number"),
    ("STYLE_LETTER",     "sub_number"),
    ("STYLE_GUIDE",     "guide"),
    ("OG_MIN",     "original_gravity_min"),
    ("OG_MAX",     "original_gravity_max"),
    ("FG_MIN",     "final_gravity_min"),
    ("FG_MAX",     "final_gravity_max"),
    ("IBU_MIN",     "bitterness_min"),
    ("IBU_MAX",     "bitterness_max"),
    ("COLOR_MIN",     "color_min"),
    ("COLOR_MAX",     "color_max"),
    ("ABV_MIN",     "alcohol_min"),
    ("ABV_MAX",     "alcohol_max"),
    ("NOTES",     "description"),
    ("PROFILE",     "profile"),
    ("INGREDIENTS",     "ingredients"),
    ("EXAMPLES",     "examples")
)
