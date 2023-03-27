from django import template

register = template.Library()  # если мы не зарегестрируем наши фильтры, то django никогда не узнает
# где именно их искать и фильтры потеряются


@register.filter(name='censor')  # регистрируем наш фильтр под именем multiply, чтоб django понимал,
# что это именно фильтр, а не простая функция
def censor(value, arg):  # первый аргумент здесь — это то значение, к которому надо применить фильтр,
    # второй аргумент — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    # l = 'спартак'
    if isinstance(value, str):  # проверяем, что value — это точно строка
        if arg in value.lower():
            v = value.lower().replace(arg, 'Реал')
            return v
        else:
            return value
    else:
        raise value
        # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон


