<%!
from webhelpers.pylonslib.secure_form import auth_token_hidden_field
%>
${auth_token_hidden_field() | n}
