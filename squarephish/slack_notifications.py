from slack_sdk.webhook import WebhookClient
import json
def notify_slack(webhook,event,email,IP=None,useragent=None):
  webhook_client = WebhookClient(webhook)
  if event=="Email Opened":
    notify_opened(webhook_client,mask_email(email),IP,useragent)
  elif event=="QR Accessed / Clicked Link":
    notify_clicked(webhook_client,mask_email(email),IP,useragent)
  elif event=="Authentication Complete":
    notify_authenticated(webhook_client,mask_email(email))
  else:
    logging.error("Unknown status to notify: " + event)

def notify_opened(webhook,email,IP,useragent):
  slack_data = {
	"attachments": [
		{
			"color": "#ffff00",
			"title": ":ocean: *Email Opened*",
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
					"value": f"{UA}"
				}
			]
		}
	]
  }
  data=json.dumps(slack_data)
  webhook.send( text = "fallback", data = data )
def notify_clicked(webhook,email,IP,useragent):
  slack_data = {
	"attachments": [
		{
			"color": "##ffa500",
			"title": ":fish: *QR Accessed / Clicked Link*",
			"fields": [
				{
					"title": "Email",
					"value": "{email}"
				},
				{
					"title": "IP Address",
					"value": "<https://whatismyipaddress.com/ip/{IP}|{IP}>"
				},
				{
					"title": "User Agent",
					"value": "{UA}"
				}
			]
		}
	]
  }
  data=json.dumps(slack_data)
  webhook.send( text = "fallback", data = data )
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
