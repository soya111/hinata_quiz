import os
import requests

from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from utils import tool

from dotenv import load_dotenv

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

load_dotenv()

channel_secret = os.environ["LINE_CHANNEL_SECRET"]
channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@csrf_exempt
def index(request):
    if request.method == 'POST':
        print(request)
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        # body = request.get_data(as_text=True)
        body = request.body

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print(
                "Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return 'OK'
    elif request.method == 'GET':
        print(request.body)
        # print(request.headers['X-Line-Signature']
        #       if request.headers['X-Line-Signature'] else "no-x-line")

        return HttpResponse("ok")


@csrf_exempt
def show_linebot_log(request):
    '''
    LineBot のログを画面上に表示させる
    :param request: ユーザのリクエスト情報
    :return: なし
    '''
    if request.method == 'GET':
        # LineBot のリクエスト情報を取得
        contents = tool.get_linebot_log()
        return HttpResponse(contents)


@csrf_exempt
def show_debug_log(request):
    '''
    デバッグ用のログを画面上に表示させる
    :param request: ユーザのリクエスト情報
    :return: なし
    '''
    if request.method == 'GET':
        # デバッグの情報を取得
        contents = tool.get_debug_log()
        return HttpResponse(contents)
