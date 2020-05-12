import datetime

from SmartDjango import Analyse
from django.views import View
from wechatpy import parse_message
from wechatpy.replies import TextReply

from Base.auth import Auth
from Base.common import WX_TOKEN, wechat_client
from Config.models import Config, CI
from User.models import UserP


class MessageView(View):
    @staticmethod
    @Analyse.r(q=['signature', 'timestamp', 'nonce', 'echostr'])
    @Auth.wechat
    def get(r):
        return r.d.echostr

    @staticmethod
    @Analyse.r(q=['signature', 'timestamp', 'nonce', UserP.openid])
    @Auth.wechat
    def post(r):
        parse_message(r.body)
        return TextReply(message='留言功能开发中……\n收到您的第%s次留言').render()


class AccessTokenView(View):
    @staticmethod
    def get(r):
        expire_time = float(Config.get_value_by_key(CI.WX_ACCESS_TOKEN_EXPIRE) or '0')
        crt_time = datetime.datetime.now().timestamp()
        if crt_time + 10 * 60 > expire_time:
            data = wechat_client.fetch_access_token()
            Config.update_value(CI.WX_ACCESS_TOKEN, data['access_token'])
            Config.update_value(CI.WX_ACCESS_TOKEN_EXPIRE, str(crt_time + data['expires_in']))
        return 0
