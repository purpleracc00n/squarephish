from slack_sdk.webhook import WebhookClient
def notify_slack(webhook,event,email,IP=None,useragent=None):
  webhook_client = WebhookClient(webhook)
  masked_email = lambda email: '*' * len(email) if len(email) <= 7 else email[:2] + '*' * (len(email) - 7) + email[-5:]
  if event=="Email Opened":
    notify_opened(webhook_client,masked_email,IP,useragent)
  elif event=="QR Accessed / Clicked Link":
    notify_clicked(webhook_client,masked_email,IP,useragent)
  elif event=="Authentication Complete":
    notify_authenticated(webhook_client,masked_email)
  else:
    logging.error("Unknown status to notify: " + event)

def notify_opened(webhook,email,IP,useragent):
  blocks = []
  blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":ocean: *Email Opened*\n*Email*\n{email}\n*Address*\n<{IP}>\n*User-Agent*\n{useragent}"
			}
		})
  webhook.send( text = "fallback", blocks = blocks )
def notify_clicked(webhook,email,IP,useragent):
  blocks = []
  blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":fish: *QR Accessed / Clicked Link*\n*Email*\n{email}\n*Address*\n<{IP}>\n*User-Agent*\n{useragent}"
			}
	})
  webhook.send( text = "fallback", blocks = blocks )
def notify_authenticated(webhook,email):
  blocks = []
  blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":shark: *Authentication Complete*\n*Email*\n{email}\n*Address*\n<{IP}>\n*User-Agent*\n{useragent}"
			}
		})
  webhook.send( text = "fallback", blocks = blocks )
