from django import template

register = template.Library()


@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    print("Current index is: {}".format(current_index))
    index = int(current_index/2)
    print("New index is: {}".format(index))
    try:
        return some_list[(str(index)) + '_completed']  # access the next element
    except Exception as e:
        print(e)
        return ''  # return empty string in case of exception
