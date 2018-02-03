from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def circle_page(page, loop=3):
    page_range = page.paginator.page_range 
    num = page.number

    s_idx = 1 if(num - loop < 0) else num - loop
    e_idx = len(page_range) if(num + loop > len(page_range)) else num + loop
    html_list = []
    html_list.append("<a href='?page={}'><<</a>".format(s_idx))
    for p_num in page_range[s_idx-1:e_idx]:
        if(p_num == num):
            html_list.append("<{}>".format(num))
        else:
            html_list.append("<a href='?page={}'><{}></a>".format(p_num, p_num))
    html_list.append("<a href='?page={}'>>></a>".format(e_idx))

    form_str = '''
        <form action=''>
            <input type='text' name='page' value={}/{}></input>
            <input type='submit' value='GO'>
        </form>
    '''.format(num, len(page_range))
    html_list.append(form_str)
    return format_html("".join(html_list))    
