from django import template

register = template.Library()


@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    current_index -= 1
    index = int(current_index / 2)
    try:
        return some_list[(str(index)) + '_completed']  # access the next element
    except Exception as e:
        print(e)
        return ''  # return empty string in case of exception


@register.filter
def index(List, i):
    return List[int(i)]
