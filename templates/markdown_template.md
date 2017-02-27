# {{ title }}

By {{author}}
{% for h in highlights %}
{# found a new chapter, print its title #}
{% if h[1] %}
{% if h[3] is not none and last != h[3] %}{% set last=h[3] %}

## {{ h[3] }}
{% endif %}

{# print the quote #}
{{ h[1] }}
{% endif %}
{% endfor %}
