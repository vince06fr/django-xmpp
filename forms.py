# -*- coding: utf-8 -*-
#
#  Copyright (c) 2009 Marcello Bontempo Salgueiro and contributors
#
#  This file is part of Django XMPP.
#
#  Django XMPP is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#


from django import forms

class loginFORM(forms.Form):
	jabber_id = forms.CharField(max_length=300)
	jabber_pwd = forms.CharField(max_length=20, widget=forms.PasswordInput)

class sendFORM(forms.Form):
	user = forms.CharField(max_length=300)
	msg = forms.CharField(widget=forms.Textarea())

class authJIDFORM(forms.Form):
	jid_auth = forms.CharField(max_length=300)

STATUS_C = (
		('Connected','Connected'),
		('Alway','Alway'),
		('Busy','Busy'),
)
class changeSTATUS(forms.Form):
	status = forms.ChoiceField(widget=forms.Select(),choices=STATUS_C)
