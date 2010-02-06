${_('Hello,')}

${_("""A request has been made to reset your password. You can change your password 
by following this link:""")}
${url('reset_password', token=c.password_token, qualified=True)}

${_("""If you did not request us to reset and email you your password, please ignore
this email.""")}

${_("""Regards,
PylonsHQ""")}
