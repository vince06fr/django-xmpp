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

import xmpp,sys
from threading import Thread
from django.utils.encoding import smart_str,smart_unicode
#from django.utils import simplejson


ROSTER ,MESSAGE, JABBER_SESSION = {},{},{}

class Thread_XMPP(Thread):
	def __init__(self,session):
		self.session = session
		super(Thread_XMPP,self).__init__(name=session.jabber_id)
		
	def run(self):
		self.finished = False
		while not self.finished:
			if self.session.conn:		
				self.session.client.Process(1)

	def stop(self):

		self.finished = True
		self.session.conn = False
		

class App_XMPP(object):
	def __init__(self, jabber_id, jabber_pwd):
		self.message = {}
		self.jid_authorize=[]
		self.roster = {}

		self.jabber_id = xmpp.protocol.JID(jabber_id)
		self.jabber_pwd = jabber_pwd
	
		self.client = xmpp.Client(self.jabber_id.getDomain(), debug=[])	
		self.conn = self.connect_xmpp()
		self.client.sendInitPresence(requestRoster=0)

		self.client.RegisterHandler('message', self.recive_msgHandler)
		self.client.RegisterHandler('presence', self.presenceHandler)

		self.initJabber = Thread_XMPP(self)
		self.initJabber.start()

	def connect_xmpp(self):
		connected = self.client.connect()
		if not connected:
			return False
		authenticated = self.client.auth(self.jabber_id.getNode(),self.jabber_pwd,resource='Web')
		if not authenticated:
			return False
		return connected
	
	def add_hashmsg(self, userfrom, usermessage, userto='None'):
#		hash_msg = self.message
		
		if self.message.has_key(userfrom):
			copy_hash = self.message[userfrom]
	#		copy_hash.append({userfrom:usermessage})
			if(userto != 'None'):
				copy_hash.append({userto:usermessage})
			else:
				copy_hash.append({userfrom:usermessage})

			self.message[userfrom]=copy_hash
		else:
			if(userto !='None'):
				self.message[userfrom]=[{userto:usermessage}]
			else:
				self.message[userfrom]=[{userfrom:usermessage}]
	
		return self.message


	def recive_msgHandler(self, session, msg):
		#print msg.getBody()
		if msg.getBody() != None:
		#	print msg
			self.add_hashmsg( str(msg.getFrom()), msg.getBody() )
				
	
	def presenceHandler(self, session, presence):		
		# This line make a if comparation if '(presence.getShow() == None)'
		# return 'online' because 'online' is true, else 'or' whatever value from 'presence.getShow()'.
    	# ( ( (presence.getShow() == None) and 'online' ) or  presence.getShow() )
		self.roster[presence.getFrom().getStripped()]= ( ((presence.getShow() == None) and 'online') or presence.getShow() )
	
		if presence.getType() == 'unavailable': del self.roster[presence.getFrom().getStripped()]
		if presence.getType() == 'subscribe':
			jid = presence.getFrom().getStripped()
			self.jid_authorize.append(jid)	

	def logout_xmpp(self):
		self.client.disconnect()
		self.initJabber.stop()
		return 'Log out'
	
	def send_msg(self, user, text):
		msg = self.client.send(xmpp.protocol.Message(user ,text))
		self.add_hashmsg(user,text,str(self.jabber_id))	
		return (user, text)

	def get_rosters(self):
		return self.client.getRoster()

	def all_roster(self):
		if self.roster:
			for off_roster in self.get_rosters().getItems():
				if (off_roster not in self.roster) and (off_roster != self.jabber_id):
					self.roster[off_roster]='offline'
		return self.roster

	def set_presence(self,priority=1,show='None',status='Connect'):
		self.client.send(xmpp.protocol.Presence(priority=priority,show=show,status=status))
	
	def authorize(self,jid):
		self.getRosters().Authorize(jid)
		self.jid_authorize.remove(jid)
		return jid

	def unauthorize(self, jid):
		self.get_Rosters().Unauthorize(jid)
		self.jid_authorize.remove(jid)
		return jid

	def subscribe(self, jid):
		self.get_Rosters.Subscribe(jid)
		return jid
	
	def unsubscribe(self,jid):
		self.get_Rosters.Unsubscribe(jid)
		return jid

