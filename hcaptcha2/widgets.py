import urllib
urlencode = urllib.urlencode

from django import forms
from django.utils.safestring import mark_safe


from .renderers import get_default_renderer

from hcaptcha2.settings import JS_API_URL, SITEKEY


class MyWidget(forms.Widget):
    def get_context(self, name, value, attrs):
        return {
            'widget': {
                'name': name,
                'is_hidden': self.is_hidden,
                'required': self.is_required,
                'value': self.format_value(value),
                'attrs': self.build_attrs(self.attrs, attrs),
                'template_name': self.template_name,
            },
        }

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a template.
        """
        if value == '' or value is None:
            return None
        if self.is_localized:
            return formats.localize_input(value)
        return str(value)



class hCaptchaWidget(MyWidget):
    template_name = 'hcaptcha2/forms/widgets/hcaptcha_widget.html'

    def __init__(self, *args, **kwargs):
        self.extra_url = {}
        super(hCaptchaWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return data.get('h-captcha-response')

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super(hCaptchaWidget, self).build_attrs(base_attrs) #, extra_attrs)
        attrs['data-sitekey'] = SITEKEY
        attrs['style'] = "text-align:right"
        return attrs

    def get_context(self, name, value, attrs):
        context = super(hCaptchaWidget, self).get_context(name, value, attrs)
        context['api_url'] = JS_API_URL
        if self.extra_url:
            context['api_url'] += '?' + urlencode(self.extra_url)
        return context

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, renderer)

    def _render(self, template_name, context, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()        
        return mark_safe(renderer.render(template_name, context))
