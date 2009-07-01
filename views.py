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

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from settings import DJANGO_MEDIA_URL
from forms import *
from xmpp_lib import *
import sha

UUID= None

def login(request):
		connected = {}
		if request.POST:
			form = loginFORM(request.POST)
			if form.is_valid():
				jid = form.cleaned_data['jabber_id']
				pwd = form.cleaned_data['jabber_pwd']
				global UUID 
				UUID = sha.new("%s%s" % (jid, pwd,)).hexdigest()
				print UUID
				global JABBER_SESSION
				JABBER_SESSION[UUID] = App_XMPP(jid,pwd)
				global MESSAGE
				MESSAGE[UUID] = JABBER_SESSION[UUID].message
				global ROSTER
				ROSTER[UUID] = JABBER_SESSION[UUID].all_roster()
				JABBER_SESSION[UUID].set_presence()
				return HttpResponseRedirect('/xmpp/'+UUID+'/roster/') 
			else:
				connected['form'] = form
				return render_to_response('django_xmpp/login.html', connected)
		else:
			connected['form'] = loginFORM()	
			return render_to_response('django_xmpp/login.html', connected)


def logout(request,uuid):
	if request:
		JABBER_SESSION[uuid].logout_xmpp()
		return HttpResponseRedirect('/xmpp/login/')

def send_message(request,uuid):
	message= {}
	if request.POST:
		form = sendFORM(request.POST)
		if form.is_valid():
			user = form.cleaned_data['user']
			text = form.cleaned_data['msg']
			try:
				msg = JABBER_SESSION[uuid].send_msg(user,text)
#				msg = JABBER_SESSION[uuid].send_msg('marcello@lerdeza',text)
			except AttributeError:
				return  HttpResponseRedirect('/xmpp/login/')
		else:
			message['form'] = sendFORM()
		message['form']=sendFORM()
	else:
		message['form']= sendFORM()

	return render_to_response('django_xmpp/send_msg.html',{'form': message['form']})

def recive_message(request,uuid):
	if MESSAGE:
		status = MESSAGE[uuid]
	else:
		status = None
	return render_to_response('django_xmpp/recive_message.html',{'status': status }) # 'form': message['form']})

def view_roster(request,uuid):
	if request:
		try:	
			roster = JABBER_SESSION[uuid].all_roster()
		except AttributeError:
			return  HttpResponseRedirect('/xmpp/login/')

		return render_to_response('django_xmpp/roster.html',{'roster': roster} )#,'DJANGO_MEDIA_URL': DJANGO_MEDIA_URL}) 

def set_status(request,uuid):
	status = {}
	st=''
	defaul_value = { 'status': st}
	if request.POST:
		form = changeSTATUS(request.POST)
		if form.is_valid():
			st=form.cleaned_data['status']
			status_lower = st.lower()
			try:
				if status_lower == 'alway': 
					JABBER_SESSION[uuid].set_presence(priority=1,show='xa',status=st)
				elif status_lower ==  'busy':
					JABBER_SESSION[uuid].set_presence(priority=1,show='dnd', status=st)
				else:
					JABBER_SESSION[uuid].set_presence(priority=1,show='avaliable',status=st)
			except AttributeError:
				return  HttpResponseRedirect('/xmpp/login/')
		else:
			st='invalid form'
		status['form']=changeSTATUS()
	else:
		status['form']=changeSTATUS()

	return render_to_response('django_xmpp/status.html',{'status':status['form'], 'st' : st } )

def authorize_view(request,uuid):
	auth_form={}
	try:	
		authorized=JABBER_SESSION[uuid].jid_authorize
	except AttributeError:
		return  HttpResponseRedirect('/xmpp/login/')

	if authorized == []:
		return HttpResponseRedirect('/xmpp/roster/')
	else:	
		default_value = { 'jid_auth': authorized[0] }
		if request.POST:
			form = authJIDFORM(request.POST)
			if form.is_valid():
				jid = form.cleaned_data['jid_auth']
				JABBER_SESSION[uuid].authorize(jid)
				return HttpResponseRedirect('/xmpp/roster/')
			else:
				auth_form['form']= authJIDFORM(default_value)

		auth_form['form']=authJIDFORM(default_value)
	return render_to_response('django_xmpp/authorized.html', {'auth': auth_form['form']} )
