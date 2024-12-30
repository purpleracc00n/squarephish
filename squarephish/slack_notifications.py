import json
import requests
from user_agents import parse

def getIPInfoData(ip_address, api_token):
  url = f"https://ipinfo.io/{ip_address}?token={api_token}"

  try:
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    isp = data.get("org", "N/A")
    country = data.get("country", "N/A")

    return {"ISP": isp, "Country": country}

  except requests.exceptions.RequestException as e:
    return {"error": str(e)}

def getUserAgentDetails(user_agent):
  try:
    ua = parse(user_agent)
        
    platform = ua.device.family
    os = f"{ua.os.family} {ua.os.version_string}"
    browser = f"{ua.browser.family} {ua.browser.version_string}"
    mobile = ua.is_mobile
        
    return {
      "Platform": platform,
      "OS": os,
      "Browser": browser,
      "Mobile": mobile
    }

  except Exception as e:
    return {"error": str(e)}

def notify_slack(webhook,ipinfo_key,event,email,IP=None,useragent=None):
  IPInfoData = getIPInfoData(IP,ipinfo_key)
  UserAgentDetails = getUserAgentDetails(useragent)
  if event=="Email Opened":
    notify_opened(webhook,mask_email(email),IP,useragent,IPInfoData,UserAgentDetails)
  elif event=="QR Accessed / Clicked Link":
    notify_clicked(webhook,mask_email(email),IP,useragent,IPInfoData,UserAgentDetails)
  elif event=="Authentication Complete":
    notify_authenticated(webhook,mask_email(email))
  else:
    logging.error("Unknown status to notify: " + event)

def notify_opened(webhook,email,IP,useragent,IPInfoData,UserAgentDetails):
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
					"title": "COUNTRY",
					"value": f"{IPInfoData['Country']}"
				},
				{
					"title": "ISP",
					"value": f"{IPInfoData['ISP']}"
				},
				{
					"title": "User Agent String",
					"value": f"{useragent}"
				},
				{
					"title": "User Agent Details",
					"value": f"Platform: {UserAgentDetails['Platform']}\nOS: {UserAgentDetails['OS']}\nBrowser: {UserAgentDetails['Browser']}\nMobile: {UserAgentDetails['Mobile']}"
				}
			]
		}
	]
  }
  requests.post(webhook, json=slack_data)
def notify_clicked(webhook,email,IP,useragent,IPInfoData,UserAgentDetails):
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
					"title": "COUNTRY",
					"value": f"{IPInfoData['Country']}"
				},
				{
					"title": "ISP",
					"value": f"{IPInfoData['ISP']}"
				},
				{
					"title": "User Agent String",
					"value": f"{useragent}"
				},
				{
					"title": "User Agent Details",
					"value": f"Platform: {UserAgentDetails['Platform']}\nOS: {UserAgentDetails['OS']}\nBrowser: {UserAgentDetails['Browser']}\nMobile: {UserAgentDetails['Mobile']}"
				}
			]
		}
	]
  }
  requests.post(webhook, json=slack_data)
def notify_authenticated(webhook,email):
  slack_data = {
	"attachments": [
		{
			"color": "#f05b4f",
			"title": ":shark: Authentication Complete",
			"fields": [
				{
					"title": "Email",
					"value": f"{email}"
				}
			]
		}
	]
  }
  requests.post(webhook, json=slack_data)
	
def mask_email(s):
    if len(s) <= 7:
        return '*' * len(s)
    else:
        return s[:2] + '*' * (len(s) - 7) + s[-5:]
