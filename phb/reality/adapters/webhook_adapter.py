import requests

class WebhookAdapter:
    def run(self, intent):
        url = intent.get("url")
        payload = intent.get("payload", {})

        r = requests.post(url, json=payload)

        return {
            "status": "sent",
            "response": r.text
        }
