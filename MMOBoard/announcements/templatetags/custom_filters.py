from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
from announcements.models import *
censor_list = []


with open ("../MMOBoard/censor_words.txt", "r") as censor_words:
    for line in censor_words:
        b = (line.strip())
        censor_list = b.split(",")
censor_words.close()


@register.filter
@stringfilter
def censor(value):

    value1 = value.lower()
    for word in censor_list:
        if word in value1:
            if word != "":
                value1 = value1.replace(word, "*" * len(word))
    list_of_value = list(value)
    uppercase_index_list = []
    for letter in list_of_value:
        if letter.isupper():
            uppercase_index_list.append(value.index(letter))
    uppercase_index_list_uniq = sorted(list(set(uppercase_index_list)))
    list_of_value1 = list(value1)
    for id, sym in enumerate(list_of_value1):
        if id in uppercase_index_list_uniq:
            list_of_value1[id] = sym.upper()
            value = "".join(list_of_value1)
    return value

@register.filter
def author(value):
    m = Profile.objects.get(id = value)
    return m

@register.filter
def category_name(value):
    if '=' in value:
        part1,part2 = value.split('=')
        return Category.objects.get(id=part2)


@register.filter
def response_counter(value):
    return len(ANCTResponse.objects.filter(announcement=value,confirm=False,refuse=False))

@register.filter
def response_counter_main_page(value):
    return len(ANCTResponse.objects.filter(author=Profile.objects.get(id=value),confirm=False,refuse=False))

@register.filter
def what_category_not_subscribed(value):
    profile = Profile.objects.get(id=value)
    profile.subscribing_categories.values_list()
    res = profile.subscribing_categories.res = profile.subscribing_categories.values_list('category',flat=True).annotate()
    for i in res:
        return ",".join([i for i in res])




@register.simple_tag
def all_categories():
    res= Category.objects.filter().values_list('category',flat=True).annotate()
    for i in res:
        return ",".join([i for i in res])

@register.filter
def path_without_pages(value):
        return value.partition('&page')[0]