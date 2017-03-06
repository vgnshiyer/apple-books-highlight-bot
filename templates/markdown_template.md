# {{ title }}

By {{author}}
{% set vars={'last': none} %}
{% for h in highlights %}
{# found a new chapter, print its title #}
{% if h[1] %}
{% if h[3] is not none and vars.last != h[3] %}
{# stupid hacky nonsense to get around assignment not holding in outer scope #}
{% if vars.update({'last': h[3]}) %}{% endif %}

## {{ h[3] }}
{% endif %}

{# print the quote #}
{{ h[1] }}{% if h[6] is not none and h[6]|length > 0 %}  _NOTE: {{ h[6] }}_{% endif %}

{% endif %}
{% endfor %}
