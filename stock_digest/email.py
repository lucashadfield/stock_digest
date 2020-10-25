import io
import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import matplotlib.pyplot as plt
import yaml


class Email:
    def __init__(self, config_path: str):
        self.config = self._load_config(Path(config_path).expanduser())

        self.msg = MIMEMultipart('alternative')
        self.host = self.config['host']
        self.port = self.config['port']
        self.username = self.config['username']
        self.password = self.config['password']

    @staticmethod
    def _load_config(config_path: Path) -> dict:
        with config_path.open() as f:
            return yaml.safe_load(f)

    def attach_fig(self, fig: plt.Figure, name: str):
        html = f'''
        <html>
           <img src="cid:image_id_1">
        </html>
        '''

        self.msg.attach(MIMEText(html, "html"))

        with io.BytesIO() as buf:
            fig.savefig(buf, format='png')
            buf.seek(0)
            img = MIMEImage(buf.read(), name=name)

        img.add_header('Content-ID', '<image_id_1>')
        self.msg.attach(img)

    def send(self, subject: str, sender: str, recipient: str):
        self.msg['Subject'] = subject
        self.msg['From'] = sender
        self.msg['To'] = recipient

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(sender, recipient, self.msg.as_string())
