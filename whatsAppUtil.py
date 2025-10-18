import os
from dotenv import load_dotenv
from twilio.rest import Client


class whatsAppUtil:
    def __init__(self):
        load_dotenv()

        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("FROM_WHATSAPP_NUMBER")
        if not all([self.account_sid, self.auth_token, self.from_number]):
            raise ValueError("❌ Missing Twilio credentials or phone numbers in .env file")

        self.client = Client(self.account_sid, self.auth_token)

    def send_image_message(self, to_number=None, image_url=None, caption=""):
        """
        Send a WhatsApp message with image and caption using Twilio
        """
        if not image_url:
            raise ValueError("❌ You must provide an image URL (requires public URL, not local file).")

        to_number = to_number

        print(f"📤 Sending WhatsApp image message to {to_number}")

        message = self.client.messages.create(
            from_=self.from_number,
            to=f"whatsapp:+{to_number}" if not str(to_number).startswith("whatsapp:") else to_number,
            body=caption,
            media_url=[image_url],
        )

        print("✅ Message sent successfully!")
        print(f"Message SID: {message.sid}")


# ------------------- TEST EXAMPLE -------------------

if __name__ == "__main__":
    util = whatsAppUtil()

    image_url = "https://images.pexels.com/photos/3873669/pexels-photo-3873669.jpeg"
    input_number = "+201142490433"
    to_number = "whatsapp:" + input_number
    caption = (
        "Hello from EXACT Team! 🎉\n"
        "Your customized photo is ready.\n"
        "We hope you love it — feel free to share it with your friends!"
    )

    util.send_image_message(to_number=to_number,image_url=image_url, caption=caption)
