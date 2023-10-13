#!/usr/bin/env python3
import json
import os
import discord
import requests
from discord.ext import commands

discord_token = os.environ["DISCORD_MCPOLITICS"]

errors = []

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'Cookie': 'cookie_consent_level=%7B%22strictly-necessary%22%3Atrue%2C%22functionality%22%3Atrue%2C%22tracking%22'
              '%3Atrue%2C%22targeting%22%3Atrue%7D; cookie_consent_user_accepted=true; '
              'unitalkies-ih=s%3Aib7TQO2x1GT-EH3t51FBIkZNd8I9ceSe.9L4n7tslwLXP46C9hyK%2FO3VB4GEUuxSyIWtdg1ded8s',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'x-token': "",
}

requestdata = {}

discord_client = commands.Bot(command_prefix='MC!', intents=discord.Intents.all(), help_command=None)

local_backurl = "http://localhost:8080/api"
official_backurl = "https://lionfish-app-tpfeq.ondigitalocean.app/api"

backurl = official_backurl


def isLoggedIn():
    _isLoggedInURL = backurl + "/auth/renew"
    _isLoggedInData = json.loads(requests.get(url=_isLoggedInURL, headers=headers).text)
    if _isLoggedInData["status"] == 999:
        return False
    else:
        print("IS ALREADY LOGGED IN")
        return True


def login():
    if not isLoggedIn():
        _url_login = backurl + "/auth/login"
        _login = json.loads(requests.post(url=_url_login, headers=headers, json={
            "username": "Martin_Sonneborn",
            "password": "123",
            "browserInformation": {
                "browserInformation": {
                    "appCodeName": 'Mozilla',
                    "appName": 'Netscape',
                    "appVersion": '5.0 (Windows)',
                    "availHeight": 1040,
                    "availWidth": 1920,
                    "buildID": '20181001000000',
                    "canvasFingerprint": '5d3310a21ca2e57dce7cb1fbb983119f',
                    "cookieEnabled": True,
                    "devicePixelRatio": 1,
                    "hardwareConcurrency": 16,
                    "height": 1080,
                    "language": 'de',
                    "languages": ['de', 'en-US', 'en'],
                    "maxTouchPoints": 0,
                    "onLine": True,
                    "oscpu": 'Windows NT 10.0; Win64; x64',
                    "pdfViewerEnabled": True,
                    "platform": 'Win32',
                    "plugins": [],
                    "product": "Gecko",
                    "productSub": '20100101',
                    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
                    "vendor": '',
                    "vendorSub": '',
                    "webdriver": False,
                    "width": 1920
                }
            }
        }).text)
        if _login['status'] == 200:
            headers['x-token'] = _login['token']
        else:
            print(f'ERROR: Cant login: "{_login["error"]}"')


@discord_client.event
async def on_ready():
    print("The Bot has started")
    login()


@discord_client.command()
async def verify(ctx):
    login()
    print(ctx.author.id)


discord_client.run(discord_token)