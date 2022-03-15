"""
Unit conversion helpers 
"""

KG_TO_LB_INDEX = 2.20462262
G_TO_OZ_INDEX = 0.0352739619
L_TO_GAL_INDEX = 0.264172052


def kg_to_lb(value):
    return float(value)*KG_TO_LB_INDEX

def lb_to_kg(value):
    return float(value)/KG_TO_LB_INDEX

def g_to_oz(value):
    return float(value)*G_TO_OZ_INDEX

def oz_to_g(value):
    return float(value)/G_TO_OZ_INDEX

def l_to_gal(value):
    return float(value)*L_TO_GAL_INDEX

def gal_to_l(value):
    return float(value)/L_TO_GAL_INDEX

def c_to_f(value):
    return float(value)*(9/5)+32

def c_to_f(value):
    return float(value)*(9./5.)+32

def f_to_c(value):
    return (float(value)-32)*5./9.

def ebc_to_srm(value):
    return float(value)*0.508

def srm_to_ebc(value):
    return float(value)*1.97

def srm_to_lovibond(value):
    return (float(value) + 0.6) / 1.35

def ebc_to_lovibond(value):
    value = ebc_to_srm(value)
    return (float(value) + 0.6) / 1.35

