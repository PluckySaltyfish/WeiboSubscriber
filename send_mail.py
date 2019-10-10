import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart

class MailSender():
    def __init__(self,from_addr,to_addr,password,from_name,to_name,subject):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.password = password
        self.mail_txt = ''
        self.from_name = from_name
        self.to_name = to_name
        self.subject = subject
        self.msg = MIMEMultipart('related')
        self.msg['From'] = formataddr([from_name, from_addr])
        self.msg['To'] = formataddr([to_name, to_addr])
        self.msg['Subject'] = self.subject

    def add_text(self,mail_txt):
        self.mail_txt += mail_txt

    def add_pics(self,pics):
        for i in pics:
            file = open('pics/' + i, "rb")
            img_data = file.read()
            file.close()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', i)
            self.msg.attach(img)
            self.mail_txt += '<img src="cid:' + i + '">'

    def send(self,smtp_server = 'smtp.qq.com'):
        ret = True
        try:
            msgTxt = MIMEText(self.mail_txt, 'html', 'utf-8')
            self.msg.attach(msgTxt)

            server = smtplib.SMTP_SSL(smtp_server, 465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(self.from_addr, self.password)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.from_addr, [self.to_addr, ], self.msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()

        except Exception as e:
            ret = False
            print('send mail failed : ',e)
        return ret

if __name__ == '__main__':
    ms = MailSender('1828151761@qq.com','1828151761@qq.com','vjfhghlcxenkcbaj','我知道你为什么傲慢<br />你到了坡上<br />心情不错<br />有些喘<br />','李诞','太阳系','李诞的微博',['xiaolin.png'])
    ms.send()