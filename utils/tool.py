# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import os

import logging

# LineBot リクエスト用のログファイルのパス
LINEBOTPATH = os.path.dirname(os.path.abspath(
    'logconfig.py')) + '/log/linelogger.txt'

# デバック用のログファイルのパス
DEBUGPATH = os.path.dirname(os.path.abspath('logconfig.py')) + '/log/debug.txt'


def get_linebot_log():
    '''
    LineBot のリクエストログの情報を取得
    :return: LineBot のリクエストログ
    '''
    contents = 'Not Contents'
    if (os.path.isfile(LINEBOTPATH)):
        with open(LINEBOTPATH, 'r', encoding='utf-8') as linebotfile:
            contents = linebotfile.read()
    return contents


def get_debug_log():
    '''
    debug の情報を取得する
    :return:
    '''
    contents = 'Not Contents'
    if (os.path.isfile(DEBUGPATH)):
        with open(DEBUGPATH, 'r', encoding='utf-8') as debugfile:
            contents = debugfile.read()
    return contents


@csrf_exempt
def out_put_log(request):
    '''
    LineBot のリクエスト情報をログ出力する
    :param request: ユーザリクエストの情報
    :return: なし
    '''

    # もしリクエストが POST の場合はファイルにリクエスト情報をファイルに保存する
    # 直接ブラウザからアクセスすると GET になる
    if request.method == 'POST':
        linelogger = logging.getLogger('rabbitBotLogging')
        # byte を string型へデコード
        linelogger.debug(json.loads(request.body.decode('utf-8')))
    return '処理完了'
