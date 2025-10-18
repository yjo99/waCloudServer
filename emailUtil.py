import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

class EmailUtil:
    def __init__(self):
        load_dotenv()

        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.image_path = os.getenv("IMAGE_PATH", "./images")

        if not all([self.sender_email, self.sender_password, self.smtp_server]):
            raise ValueError("❌ Missing required SMTP configuration in .env file")

    def send_images_by_names(self, to_email, subject, body, image_names):
        """
        Send specific images by name from the configured IMAGE_PATH folder.

        :param to_email: receiver email address
        :param subject: email subject
        :param body: email body
        :param image_names: list of image filenames (e.g., ["a.jpg", "b.png"])
        """
        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        attached_count = 0

        for image_name in image_names:
            image_file = os.path.join(self.image_path, image_name)

            if not os.path.exists(image_file):
                print(f"⚠️ Image not found: {image_file}")
                continue

            with open(image_file, "rb") as f:
                img_data = f.read()

            msg.add_attachment(
                img_data,
                maintype="image",
                subtype=image_name.split(".")[-1],
                filename=image_name
            )
            attached_count += 1

        if attached_count == 0:
            print("⚠️ No valid images found to send.")
            return

        # Send the email
        print(f"📤 Connecting to {self.smtp_server}:{self.smtp_port} ...")
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(self.sender_email, self.sender_password)
            smtp.send_message(msg)
            print(f"✅ Email sent successfully! ({attached_count} image(s) attached)")

# ---------- Test Example ----------
if __name__ == "__main__":
    util = EmailUtil()

    # Example: take image names from "customer input"
    customer_images = ["pyramids_1.jpg", "pyramids2.jpg"]  # pretend these come from user input

    util.send_images_by_names(
        # to_email="ismaildahshan@gmail.com",
        to_email="yousefeldahshan6@gmail.com",

        subject="Your Kiosak Photo Is Ready!",
        body='''Hello,
\n
Thank you for using Kiosak! 🎉 
Your customized photo is ready and attached below.
\n
We hope you love your photo — feel free to share it with your friends and tag us online!  
If you have any feedback or issues, we’d love to hear from you.
\n
Best regards,  
The Kiosak Team  
        ''',
        image_names=customer_images
    )
