import requests
import json

# # payload = {"files":["/Users/psemp/Documents/GitHub/crowAIchatbots/data/Css_Notes__1689837440.pdf"]}
url = "https://9w6lw.apps.beam.cloud"
payload = {"files":["/Users/psemp/Documents/GitHub/crowAIchatbots/data/Css_Notes__1689837440.pdf"]}
headers = {
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate",
  "Authorization": "Basic NTM5ODNiNzdkMGU2ZjI4MWMwOWU0ZTIyOTQyMTE4NWY6ZWM4M2I1ZWQ0MmRjOGE5ZTUwN2FlMWJlNWJmOTU2YmQ=",
  "Connection": "keep-alive",
  "Content-Type": "application/json"
}

response = requests.request("POST", url,
  headers=headers,
  data=json.dumps(payload)
)



