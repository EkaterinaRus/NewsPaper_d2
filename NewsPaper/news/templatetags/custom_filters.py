from django import template
import re

register = template.Library()  # если мы не зарегестрируем наши фильтры, то django никогда не узнает
# где именно их искать и фильтры потеряются


@register.filter(name='censor')  # регистрируем наш фильтр под именем multiply, чтоб django понимал,
# что это именно фильтр, а не простая функция
def censor(value, arg):  # первый аргумент здесь — это то значение, к которому надо применить фильтр,
    # второй аргумент — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    res = re.sub(r'(?i)хуй(?=\W)', arg, value)
    res1 = re.sub(r'(?i)блять(?=\W)', arg, res)
    return res1


