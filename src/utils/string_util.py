import base64


def cook_element(element: tuple, *value):
    locator, element = element
    return locator, str(element).format(*value)


def decode(encrypted_value):
    return base64.b64decode(encrypted_value).decode('utf-8')
