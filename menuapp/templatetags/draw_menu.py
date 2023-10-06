from django import template
from django.urls import reverse
from menuapp.models import Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context["request"]
    current_path = request.path

    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return ""

    def render_menu(menu_item):
        active = "active" if current_path == menu_item.url else ""
        children = menu_item.children.all()

        if children:
            submenu_html = "<ul>"
            for child in children:
                submenu_html += render_menu(child)
            submenu_html += "</ul>"
        else:
            submenu_html = ""

        if menu_item.url.startswith("/"):
            url = menu_item.url
        else:
            url = reverse(menu_item.url)

        return f'<li class="{active}"><a href="{url}">{menu_item.name}</a>{submenu_html}</li>'

    menu_html = f'<h1>{menu.name}</h1> <ul class="menu">'
    
    for item in menu.children.all():
        menu_html += render_menu(item)
    menu_html += "</ul>"

    return menu_html
