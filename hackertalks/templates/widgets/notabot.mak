<%namespace name="tw" module="tw.core.mako_util"/>\
<%!
from webhelpers.rails.urls import js_obfuscate
%>
${js_obfuscate('<input type="hidden" name="notabot" %s' % tw.attrs(attrs=attrs)) | n}