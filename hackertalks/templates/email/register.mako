${_("Welcome to PylonsHQ!")}

${_("""Thanks for signing up. To finish activating your account, you will need
to verify your email address. Please click on the link below to confirm
your email address.""")}

${url('verify_email', token=c.email_token, qualified=True)}

${_("""If you're unable to click on the link, copy and paste the entire url
into the address window of your web browser.""")}

- PylonsHQ
