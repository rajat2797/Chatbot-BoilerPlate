from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from credentials import *
import requests, json

VERIFY_TOKEN = verify_token
PAGE_ACCESS_TOKEN = page_access_token

def logg(text,symbol='*'):
	print '%s%s%s'%(symbol*10,text.symbol*10)

def handle_quickreply(fbid, payload):
	pass

def handle_postback(fbid,payload):
	pass

def post_fb_msg(fbid,message):
	post_fb_url='https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": message }})
	status = requests.post(post_fb_url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

class MyChatBotView(generic.View):
	def get(self,request,*args,**kwargs):
		if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('oops invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self,request,*args,**kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		incoming_message=json.loads(self.request.body.decode('utf-8'))
		logg(incoming_message)
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				logg(message)
				try:
					if 'postback' in message:
						handle_postback(message['sender']['id'],message['postback']['payload'])
						return HttpResponse()
					else:
						pass
				except Exception as e:
					logg(e,symbol='-51-')

				try:
					if 'quick_reply' in message['message']:
						handle_quickreply(message['sender']['id'],message['message']['quick_reply']['payload'])
						return HttpResponse()

				except Exception as e:
					logg(e,symbol='-59-')

				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					post_fb_msg(sender_id,message_text)
				
				except Exception as e:
					logg(e,symbol='-66-')

		return HttpResponse()

def index(request):
	return HttpResponse('HI')