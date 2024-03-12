from slack_sdk.webhook import WebhookClient
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
  blocks = []
  blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":ocean: *Email Opened*\n*Email*\n{email}\n*Address*\n<https://whatismyipaddress.com/ip/{IP}|{IP}>\n*User-Agent*\n{useragent}"
			}
		})
  webhook.send( text = "fallback", blocks = blocks )
def notify_clicked(webhook,email,IP,useragent):
  blocks = []
  blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":fish: *QR Accessed / Clicked Link*\n*Email*\n{email}\n*Address*\n<https://whatismyipaddress.com/ip/{IP}|{IP}>\n*User-Agent*\n{useragent}"
			}
	})
  webhook.send( text = "fallback", blocks = blocks )
def notify_authenticated(webhook,email):
  blocks = []
  blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":shark: *Authentication Complete*\n*Email*\n{email}\n*Address*\n<https://whatismyipaddress.com/ip/{IP}|{IP}>\n*User-Agent*\n{useragent}"
			}
		})
  webhook.send( text = "fallback", blocks = blocks )
	
def mask_email(s):
    if len(s) <= 7:
        return '*' * len(s)
    else:
        return s[:2] + '*' * (len(s) - 7) + s[-5:]
