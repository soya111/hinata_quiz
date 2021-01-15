# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

import os
import logging
import json
import random
import requests
# import log.logconfig
from utils import tool
from dotenv import load_dotenv

from .models import Quiz, Choice, Nonce, UserInfo

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer,
    ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage
)


# デバッグ用のログを出す
logger = logging.getLogger('commonLogging')


load_dotenv()

channel_secret = os.environ["LINE_CHANNEL_SECRET"]
channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# bot メイン処理


@csrf_exempt
def index(request):

    # デバッグ用
    # logger.debug('index start')

    # リクエストが Post のみ
    if request.method == 'POST':
        reply = ''

        # get X-Line-Signature header value
        x_line_signature = request.headers['X-Line-Signature']

        # get request body
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            handler.handle(body, x_line_signature)
        except InvalidSignatureError:
            print(
                "Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        # リクエスト取得
        request_json = json.loads(body)

        # LineBot ログの出力
        # out_log = tool.out_put_log(request)

        try:
            # リクエストが空でないことを確認
            if(request_json != None):

                # イベントの取得
                for event in request_json['events']:
                    reply_token = event['replyToken']
                    logger.debug(event)
                    if event['type'] == 'message':
                        message_type = event['message']['type']

                        if message_type == 'text':
                            text = event['message']['text']
                            handle_text(event['message'],
                                        reply_token, event['source'])
                        elif message_type == 'image':
                            line_bot_api.reply_message(
                                reply_token, TextSendMessage(text='画像'))
                        elif message_type == 'sticker':
                            line_bot_api.reply_message(
                                reply_token, TextSendMessage(text='スタンプ'))
                        # elif message_type == 'video':
                        #     line_bot_api.reply_message(
                        #         reply_token, TextSendMessage(text=event['message']))
                        # elif message_type == 'audio':
                        #     line_bot_api.reply_message(
                        #         reply_token, TextSendMessage(text=event['message']))
                        # elif message_type == 'location':
                        #     line_bot_api.reply_message(
                        #         reply_token, TextSendMessage(text=event['message']))
                        else:
                            line_bot_api.reply_message(
                                reply_token, TextSendMessage(text=str(event)))
                    elif event['type'] == 'follow':
                        line_bot_api.reply_message(
                            reply_token, TextSendMessage(text='フォローありがとうございます'))
                    elif event['type'] == 'unfollow':
                        logger.debug(event)
                    elif event['type'] == 'postback':
                        handle_postback(eval(event['postback']['data']),
                                        reply_token, event['source'], request)
                    elif event['type'] == 'accountLink':
                        handle_account_link_event(
                            event['link'], reply_token, event['source'])

        except LineBotApiError as e:
            print("Got exception from LINE Messaging API: %s\n" % e.message)
            for m in e.error.details:
                print("  %s: %s" % (m.property, m.message))
            print("\n")
        except InvalidSignatureError as e:
            print(e)
            abort(400)
        except Exception as e:
            print(e)

        # デバッグ用
        # logger.debug('index end')
        # ステータスコード 200 を返却
        return HttpResponse(status=200)

    elif request.method == 'GET':
        return HttpResponseRedirect(reverse('quiz-list'))


def handle_text(message, reply_token, source):
    if message['text'] == 'クイズ':
        actions = [
            PostbackAction(label='クイズスタート', data='{"type":"push_quiz"}'),
            URIAction(label='クイズ投稿',
                      uri='https://hinatazaka46.herokuapp.com/'),
        ]

        user_id = source['userId']

        try:
            user_info = UserInfo.objects.get(line_id=user_id)
            actions += [PostbackAction(label='アカウント連携解除',
                                       data='{"type":"account_linkage_cancellation_confirm"}')]
        except ObjectDoesNotExist as e:
            print(e)
            actions += [PostbackAction(label='アカウント連携',
                                       data='{"type":"account_linkage"}')]

        buttons_template = ButtonsTemplate(
            title='日向坂46クイズ',
            text='日向坂46の知識を試そう！',
            thumbnail_image_url='https://cdn.hinatazaka46.com/images/14/f83/e7263bcddc5eee48b45337ace26dd.jpg',
            actions=actions
        )
        template_message = TemplateSendMessage(
            alt_text='日向坂46クイズ', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)

    else:
        pass


def handle_postback(data, reply_token, source, request):
    if data['type'] == 'push_quiz':
        push_quiz(reply_token)
    elif data['type'] == 'quiz_answer':
        if data['is_correct'] == True:
            push_correct_message(reply_token)
        else:
            push_incorrect_message(reply_token)
    elif data['type'] == 'account_linkage':
        push_account_linkage_message(data, reply_token, source, request)
    elif data['type'] == 'account_linkage_cancellation_confirm':
        push_account_linkage_cancellation_confirm_message(
            data, reply_token, source)
    elif data['type'] == 'account_linkage_cancellation':
        push_account_linkage_cancellation_message(
            data, reply_token, source)
    else:
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=str(data)))


def push_quiz(reply_token):
    quiz = Quiz.objects.filter(is_approved=True).filter(
        is_public=True).order_by('?')[:1][0]
    choices = quiz.get_choices()

    buttons_template = ButtonsTemplate(
        title=quiz.title,
        text=quiz.statement,
        thumbnail_image_url=quiz.thumbnail_image_url,
        actions=[
            PostbackAction(
                label=choice.text,
                text=choice.text,
                data=str({
                    "type": "quiz_answer",
                    "is_correct": choice.is_correct
                })
            ) for choice in choices
        ]
    )
    template_message = TemplateSendMessage(
        alt_text='日向坂46クイズ', template=buttons_template)
    line_bot_api.reply_message(reply_token, template_message)


def push_correct_message(reply_token):
    thumbnail_image_urls = [
        "https://cdn.wikiwiki.jp/to/w/hinataword/%E3%81%8D/::ref/n2i9190225-0129250941.jpg?rev=ed2646f5723297906ad82132767b837d&t=20190414223603",
        "https://assets.st-note.com/production/uploads/images/23190065/9a9ea2c99ee461448d4504158c495111.jpeg?fit=bounds&format=jpeg&height=500&quality=45&width=500",
        "https://i.pinimg.com/originals/89/2a/80/892a8092f71495fa42d6d3c9b28ca1e4.jpg",
        "https://pbs.twimg.com/media/ETujOv7U8AEM6b0.jpg"
    ]

    buttons_template = ButtonsTemplate(
        title='正解！',
        text='おめでとう！',
        thumbnail_image_url=random.sample(thumbnail_image_urls, 1)[0],
        actions=[
            PostbackAction(
                label='次のクイズへ',
                text='次のクイズへ',
                data=str({
                    "type": "push_quiz"
                })
            )
        ]
    )
    template_message = TemplateSendMessage(
        alt_text='日向坂46クイズ', template=buttons_template)

    line_bot_api.reply_message(reply_token, template_message)


def push_incorrect_message(reply_token):
    thumbnail_image_urls = [
        "https://pbs.twimg.com/media/EZWwMCZU4AAV6MJ.jpg:small",
        "https://pbs.twimg.com/media/ESVoYVwUMAAiA3M.jpg",
        "https://i.pinimg.com/736x/b8/00/3f/b8003fc2c0546eb9915b336537b2100a.jpg",
        "https://pbs.twimg.com/media/EFFSFdpVAAAJnJj.jpg",
        "https://i.pinimg.com/originals/3a/cc/41/3acc41594cd42c761e88cab691e67048.jpg",
        "https://i.pinimg.com/originals/14/9a/63/149a63462b049c46fc1a81eac4ecc2ea.jpg"
    ]

    buttons_template = ButtonsTemplate(
        title='不正解',
        text='残念～',
        thumbnail_image_url=random.sample(thumbnail_image_urls, 1)[0],
        actions=[
            PostbackAction(
                label='次のクイズへ',
                text='次のクイズへ',
                data=str({
                    "type": "push_quiz"
                })
            )
        ]
    )
    template_message = TemplateSendMessage(
        alt_text='日向坂46クイズ', template=buttons_template)

    line_bot_api.reply_message(reply_token, template_message)


def push_account_linkage_message(data, reply_token, source, request):
    endpoint = 'https://api.line.me/v2/bot/user/{}/linkToken'.format(
        source['userId'])
    headers = {
        'Authorization': 'Bearer {}'.format(channel_access_token)
    }
    try:
        r = requests.post(endpoint, headers=headers)
    except e:
        print(e)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text='エラーが発生しました。'))

    link_token = json.loads(r.text)['linkToken']

    url = '{}://{}/'.format('https' if request.is_secure()
                            else 'http', request.get_host())

    # url = 'https://hinatazaka46.herokuapp.com/'

    buttons_template = ButtonsTemplate(
        text="アカウント認証",
        actions=[
            URIAction(label='アカウント認証リンク',
                      uri='{}login/?linkToken={}'.format(url, link_token)),
        ]
    )
    template_message = TemplateSendMessage(
        alt_text='アカウント認証', template=buttons_template)
    line_bot_api.reply_message(reply_token, template_message)


def handle_account_link_event(data, reply_token, source):
    if data['result'] == 'ok':
        nonce = Nonce.objects.get(nonce=data['nonce'])
        user_info = UserInfo.objects.get_or_create(
            user=nonce.user, line_id=source['userId'])

        buttons_template = ButtonsTemplate(
            text="{}さんのアカウント認証が完了しました。".format(nonce.user.username),
            actions=[
                URIAction(label='アカウント確認',
                          uri='https://hinatazaka46.herokuapp.com/account/'),
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='アカウント認証完了', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)
    elif data['result'] == 'failed':
        buttons_template = ButtonsTemplate(
            text="アカウント認証に失敗しました。",
            actions=[
                PostbackAction(label='やり直す',
                               data='{"type":"account_linkage"}'),
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='アカウント認証失敗', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)


def push_account_linkage_cancellation_confirm_message(data, reply_token, source):
    text = 'アカウント連携を解除しますか？'
    confirm_template = ConfirmTemplate(
        text=text,
        actions=[
            PostbackAction(
                label='解除する', data='{"type":"account_linkage_cancellation"}'),
            MessageAction(label='解除しない', text='解除しない')
        ]
    )
    template_message = TemplateSendMessage(
        alt_text=text, template=confirm_template)
    line_bot_api.reply_message(reply_token, template_message)


def push_account_linkage_cancellation_message(data, reply_token, source):
    user_id = source['userId']
    try:
        user_info = UserInfo.objects.get(line_id=user_id)
    except ObjectDoesNotExist as e:
        print(e)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text='エラーが発生しました。'))

    user_info.delete()
    line_bot_api.reply_message(
        reply_token, TextSendMessage(text='アカウント連携が解除されました。'))
