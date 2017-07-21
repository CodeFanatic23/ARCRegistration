from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def dictKeys(dictionary):
    keys = []
    for i in dictionary:
    	keys.append(i)
    # keys.sort();
    # ans = []
    # for i in keys:
    # 	ans.append(i[1:])
    return keys

@register.filter
def getkeyValues(dictionary,key):
	values = []
	for i in dictionary[key]:
		values.append(dictionary[key][i])
	return values;