import json
import requests
def notify_slack(webhook,event,email,IP=None,useragent=None):
  if event=="Email Opened":
    notify_opened(webhook,mask_email(email),IP,useragent)
  elif event=="QR Accessed / Clicked Link":
    notify_clicked(webhook,mask_email(email),IP,useragent)
  elif event=="Authentication Complete":
    notify_authenticated(webhook,mask_email(email))
  else:
    logging.error("Unknown status to notify: " + event)

def notify_opened(webhook,email,IP,useragent):
  slack_data = {
	"attachments": [
		{
			"color": "#ffff00",
			"title": ":ocean: Email Opened",
			"fields": [
				{
					"title": "Email",
					"value": f"{email}"
				},
				{
					"title": "IP Address",
					"value": f"<https://whatismyipaddress.com/ip/{IP}|{IP}>"
				},
				{
					"title": "User Agent",
					"value": f"{useragent}"
				}
			]
		}
	]
  }
  requests.post(webhook, json=slack_data)
def notify_clicked(webhook,email,IP,useragent):
  slack_data = {
	"attachments": [
		{
			"color": "#ffa500",
			"title": ":fish: QR Accessed / Clicked Link",
			"fields": [
				{
					"title": "Email",
					"value": f"{email}"
				},
				{
					"title": "IP Address",
					"value": f"<https://whatismyipaddress.com/ip/{IP}|{IP}>"
				},
				{
					"title": "User Agent",
					"value": f"{useragent}"
				}
			]
		}
	]
  }
  requests.post(webhook, json=slack_data)
def notify_authenticated(webhook,email):
  blocks = []
  blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":shark: *Authentication Complete*\n*Email*\n{email}"
			}
		})
  webhook.send( text = "fallback", blocks = blocks )
	
def mask_email(s):
    if len(s) <= 7:
        return '*' * len(s)
    else:
        return s[:2] + '*' * (len(s) - 7) + s[-5:]
