from slack_sdk.webhook import WebhookClient

def notify_slack(event,IP=None,useragent=None,email):
  webhook_client = WebhookClient(config.get("SLACK_WEBHOOK", val))
  masked_email = lambda email: '*' * len(email) if len(email) <= 7 else email[:2] + '*' * (len(email) - 7) + email[-5:]
  if event=="Email Opened":
    notify_opened(webhook_client,IP,useragent,masked_email)
  elif event=="QR Accessed / Clicked Link":
    notify_clicked(webhook_client,IP,useragent,masked_email)
  elif event=="Authentication Complete":
    notify_authenticated(webhook_client,masked_email)
  else:
    logging.error("Unknown status to notify: " + event)

def notify_clicked(webhook,IP,useragent,email):
  blocks = []
  blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":ocean: *Email Opened*\n*Email*\n{email}\n*Address*\n{IP}\n*User-Agent*\n{useragent}"
			}
		})
