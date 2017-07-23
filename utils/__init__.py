from __future__ import unicode_literals

try:
    text_type = unicode
except NameError:  # py3
    text_type = str

def convert_utf8_dict_to_dict(dict_to_convert):
    """convert the utf-8 coded JSON dict
    coming back from requests to a normal decoded one
    """
    if isinstance(dict_to_convert, dict):
        try:
            return dict(
            (convert_utf8_dict_to_dict(key), convert_utf8_dict_to_dict(value)) for key, value in
            dict_to_convert.iteritems())
        except AttributeError: # python3
            return dict(
                (convert_utf8_dict_to_dict(key), convert_utf8_dict_to_dict(value)) for key, value in
                dict_to_convert.items())
    elif isinstance(dict_to_convert, list):
        return [convert_utf8_dict_to_dict(element) for element in dict_to_convert]
    elif isinstance(dict_to_convert, str):
        return dict_to_convert
    elif isinstance(dict_to_convert, text_type):
        return dict_to_convert.encode('ascii', 'ignore')
    else:
        return dict_to_convert