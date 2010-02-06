<%namespace name="tw" module="tw.core.mako_util"/>\
<div class="yui_autocomplete_holder">\
<input ${tw.attrs(
    [('type', context.get('type')),
     ('name', name),
     ('class', css_class),
     ('id', context.get('id')),
     ('value', value)],
    attrs=attrs
)} />\
<div id="${id}_autocomplete" class="yui_autocomplete"></div>\
</div>