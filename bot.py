import requests
from bs4 import BeautifulSoup
import time
import json
import discord
from discord.ext import commands
import asyncio
import random
import datetime

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
cookies = {'urlgen':'"{\"2001:b011:d004:1d66:b533:ce46:cdca:8459\": 3462\054 \"2001:b011:d004:32af:bda7:46c0:8724:4b4b\": 3462\054 \"180.217.202.155\": 24157\054 \"2001:b011:d004:3ac0:b5f7:81ac:b0be:3179\": 3462}:1k5sPy:66Q9ah_-dJGxae4ViS6_CnKvxt8"', 'csrftoken':'1URzCuiIuRnvDxE3wkE2BZ6ETxjUppU7', 'fbsr_124024574287414':'-KHFfXl0c8tXYJTEAp8fv14C92XOflBSxg8wxtCkl9w.eyJ1c2VyX2lkIjoiMTAwMDAzOTYxNDMwOTY5IiwiY29kZSI6IkFRQTFqYjhLRVl5WThUdkRWTUFkdU95dWNka1dvb0RIeVpvbXlMYUwtTmQwT29iaEJLc1hLYzVibWI1UUkyTFRuclRaMmt2TkJIREk5OFdWRGNTSVlTbm15SHlFb3RuY3lMQmlUQ2ZLS0ZNdjFoQXM0YkZJUi01YTlvblBkX2dac0FQVmZTMmVTQ0cyM3lxUm9OMFVYNmR2c08tWFJyX256RVhfVE4yeGh6Y3kxd0ZYcTVmV0xqa29iM2VrUE5CYkFIOEJVOVBXV1ZOVklCUkUzZzh3U0FOdXJCeldMUWhoWWg2bkpCQUdxX3ptS0M3VGNaSnQxNWVzS2d5RzJyYW54UUhRQVVjWUFod3d6TFVETnRkZFZCZWZWem1uMnhjSTlGTmVSZGxzUWhodjVELUF0WFhVeEdXZm1yNVl3X1pHdkpSaGRKYVo4OVk4WW5NUm9HaHNRdTJpWl9aLW5BejJObEpoWndDclZwOURIZyIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQkFIdklXNDU5Z3RxeDA2MnBxU0tOV3F3Um85TWJROVJHaHA1bDRPeTA3aTBYeEtWamhOQXFmaE56MVpBVGhzc3J6MkNOVG11M3JQb0V3aUJBd2gwdXFlc2s0NlpDQ0ZaQVVIbnpXWkFHQXFCejZBOFlaQ3dRWXJhYXphVFpBdm9oYU8wdWFiU0ZVTlV0aWdxN1pDWGtxbEdxSFczY2taQ0RTVkpoUzBxalpDeXNDIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1OTcyNDQ4ODB9', 'rur':'ATN', 'fbm_124024574287414':'base_domain=.instagram.com', 'shbid':'19998', 'ds_user_id':'2025572310', 'ig_did':'ATN', 'shbid':'4B28AB76-ABC1-4355-B559-035560F6B555', 'sessionid':'2025572310%3AuNrJgyEPuM4Mua%3A14', 'mid':'XOJfwQALAAF16c-sL-7SerjK3buf', 'shbts':'1597071477.4778078'}
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot is ready.')

async def igstory():
    await bot.wait_until_ready()
    channel = bot.get_channel(741147398587285524)
    name_list = []
    memeber = json.loads(requests.get('https://spreadsheets.google.com/feeds/cells/14JdHOAcG_RlDXh34o0FonQVHhOVqVNJpj_9jjQCdtYY/1/public/values?alt=json').text)
    memeber_len = len(memeber['feed']['entry'])-1
    while memeber_len > 1:
        name_list.append(memeber['feed']['entry'][memeber_len]['content']['$t'])
        memeber_len -= 2
    print(name_list)
    while not bot.is_closed():
        record = json.loads(requests.get('https://spreadsheets.google.com/feeds/cells/14ZolQJeHeP3JzKT_Eiy3w1KUtB4Q9HkT-M3cETjQDnQ/1/public/values?alt=json').text)
        sheet_len = len(record['feed']['entry'])-1
        # print(record)
        id_list = []
        while sheet_len > 1:
            id_list.append(record['feed']['entry'][sheet_len]['content']['$t'])
            sheet_len -= 2
        # print(id_list)
        for name in name_list:
            url = 'https://www.instagram.com/'+name+'/?hl=zh-tw'
            # print(url)
            r = requests.get(url, headers=headers, cookies=cookies)
            soup = BeautifulSoup(r.text, 'html.parser')
            scriptlist = soup.find_all('script')
            shareData = scriptlist[4]
            # print(shareData)
            try:
                jsondata = json.loads(shareData.string.replace('window._sharedData = ', '').replace(';', ''))
            except json.decoder.JSONDecodeError:
                shareData = scriptlist[3]
                jsondata = json.loads(shareData.string.replace('window._sharedData = ', '').replace(';', ''))
            # print(jsondata)
            reel_id = jsondata['entry_data']['ProfilePage'][0]['logging_page_id'].replace('profilePage_', '')
            for info in jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
                post = info['node']
                post_id = post['id']
                link = 'https://www.instagram.com/p/' + post['shortcode']
                if post_id not in id_list:
                    requests.get('https://docs.google.com/forms/u/0/d/e/1FAIpQLSeK6MTUl4pYTFQBcEfO631scZDgpwc0YHZ-1NtQ8gYk6YICKg/formResponse?entry.9634692=' + post_id + '&fvv=1&draftResponse=%5Bnull%2Cnull%2C%22-2039842183786340156%22%5D%0D%0A&pageHistory=0&fbzx=-2039842183786340156')
                    await channel.send(link)
            story_url = 'https://www.instagram.com/graphql/query/?query_hash=90709b530ea0969f002c86a89b4f2b8d&variables=%7B%22reel_ids%22%3A%5B%22' + reel_id + '%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22%22%2C%22stories_video_dash_manifest%22%3Afalse%7D'
            r = requests.get(story_url, headers=headers, cookies=cookies).text
            story_data = json.loads(r)
            story_list = []
            try:
                for i in story_data['data']['reels_media'][0]['items']:
                    story_id = i['id']
                    takentime = i['taken_at_timestamp']+28800
                    if story_id not in id_list:
                        try:
                            embed = discord.Embed(title=name,
                                                  description=f'來自{name}限時動態的影片',
                                                  url=i['video_resources'][len(i['video_resources']) - 1]['src'],
                                                  color=0xd327a5)
                            embed.set_footer(text=datetime.datetime.fromtimestamp(takentime))
                            embed.set_image(url=i['display_url'])
                            await channel.send(embed=embed)
                            # await channel.send(i['video_resources'][len(i['video_resources']) - 1]['src'])
                            # pass
                        except KeyError:
                            # pass
                            embed = discord.Embed(title=name,
                                                  description=f'來自{name}限時動態的照片',
                                                  url=i['display_url'],
                                                  color=0xd327a5)
                            embed.set_footer(text=datetime.datetime.fromtimestamp(takentime))
                            embed.set_image(url=i['display_url'])
                            await channel.send(embed=embed)
                            # await channel.send(i['display_url'])
                        requests.get('https://docs.google.com/forms/u/0/d/e/1FAIpQLSeK6MTUl4pYTFQBcEfO631scZDgpwc0YHZ-1NtQ8gYk6YICKg/formResponse?entry.9634692=' + story_id + '&fvv=1&draftResponse=%5Bnull%2Cnull%2C%22-2039842183786340156%22%5D%0D%0A&pageHistory=0&fbzx=-2039842183786340156')
            except IndexError:
                pass

        await asyncio.sleep(random.randint(3500, 3700))
bot.loop.create_task(igstory())

bot.run('NzIyMDY2NDIyNTY5NzYyOTU3.Xudqwg.ENFlFRnSqTYJf9Dg4g7yQUNHBeA')