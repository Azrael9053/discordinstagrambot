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
cookies1 = {yourcookies)
cookies2 = {yourcookies)

bot = commands.Bot(command_prefix='!')
memberdic = {'1022_ririchinn':763620695594237952, 'riyuki_1107':763620581001134090, 'miamia_blog':763621580605358080, 'setoaina_luna':763620923667382313, '_c0q0c_':763623068290646038, 'kara_0921_':763623068290646038, 'nemurihime_luna':763621038352367646, 'hatsuki_luna':763620847645622302, 'raisu_yawara1023':763622868654751754, 'rey__solu':763622910673027073, 'yura_yura1015':763622971415461929, 'nh__solu':763622944638894080, 'erina_taiwandj':763806234775912461, 'coastaaaaaant':763806234775912461,
             'sugar_mermaid1102':763798648277958697, 'yomizu_0208':763798648277958697, 'mermaidmarchen_ruru':763798648277958697, 'yukibi_010':763798648277958697, 'moon._.717':763798648277958697, 'momoka_solu':772340625823498250, 'mana_ikoma0618':772340597482455080}


@bot.event
async def on_ready():
    print('Bot is ready.')

async def igstory():
    await bot.wait_until_ready()
    while not bot.is_closed():
        name_list = []
        luna_list = []
        luna_member = json.loads(requests.get(
            'https://spreadsheets.google.com/feeds/cells/1FGAEw230XyCeHlRQMmMuW-GOtP_3XD6v4-TXQybrA0Q/1/public/values?alt=json').text)
        luna_len = len(luna_member['feed']['entry']) - 1
        memeber = json.loads(requests.get(
            'https://spreadsheets.google.com/feeds/cells/14JdHOAcG_RlDXh34o0FonQVHhOVqVNJpj_9jjQCdtYY/1/public/values?alt=json').text)
        memeber_len = len(memeber['feed']['entry']) - 1
        while luna_len > 1:
            luna_list.append(luna_member['feed']['entry'][luna_len]['content']['$t'])
            luna_len -= 2
        while memeber_len > 1:
            name_list.append(memeber['feed']['entry'][memeber_len]['content']['$t'])
            memeber_len -= 2
        print(name_list)
        print(luna_list)
        channel = bot.get_channel(758347213533085757)
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
            print(url)
            print(channel)
            r = requests.get(url, headers=headers, cookies=cookies1)
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
            full_name = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
            for info in jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
                post = info['node']
                post_id = post['id']
                post_text = post['edge_media_to_caption']['edges'][0]['node']['text']
                link = 'https://www.instagram.com/p/' + post['shortcode']
                if post_id not in id_list:
                    requests.get('https://docs.google.com/forms/u/0/d/e/1FAIpQLSeK6MTUl4pYTFQBcEfO631scZDgpwc0YHZ-1NtQ8gYk6YICKg/formResponse?entry.9634692=' + post_id + '&fvv=1&draftResponse=%5Bnull%2Cnull%2C%22-2039842183786340156%22%5D%0D%0A&pageHistory=0&fbzx=-2039842183786340156')
            story_url = 'https://www.instagram.com/graphql/query/?query_hash=90709b530ea0969f002c86a89b4f2b8d&variables=%7B%22reel_ids%22%3A%5B%22' + reel_id + '%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22%22%2C%22stories_video_dash_manifest%22%3Afalse%7D'
            r = requests.get(story_url, headers=headers, cookies=cookies1).text
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
                                                  # timestamp=datetime.datetime.fromtimestamp(takentime),
                                                  color=0xd327a5)
                            embed.set_footer(text=datetime.datetime.fromtimestamp(takentime))
                            embed.set_image(url=i['display_url'])
                            # await channel.send(embed=embed)
                            # pass
                        except KeyError:
                            # pass
                            embed = discord.Embed(title=name,
                                                  description=f'來自{name}限時動態的照片',
                                                  url=i['display_url'],
                                                  # timestamp=datetime.datetime.fromtimestamp(takentime),
                                                  color=0xd327a5)
                            embed.set_footer(text=datetime.datetime.fromtimestamp(takentime))
                            embed.set_image(url=i['display_url'])
                        #     await channel.send(embed=embed)
                        requests.get('https://docs.google.com/forms/u/0/d/e/1FAIpQLSeK6MTUl4pYTFQBcEfO631scZDgpwc0YHZ-1NtQ8gYk6YICKg/formResponse?entry.9634692=' + story_id + '&fvv=1&draftResponse=%5Bnull%2Cnull%2C%22-2039842183786340156%22%5D%0D%0A&pageHistory=0&fbzx=-2039842183786340156')
            except IndexError:
                pass

        channel = bot.get_channel(758347213533085757)
        zcount = 0
        for name in luna_list:
            channel = bot.get_channel(memberdic[name])
            url = 'https://www.instagram.com/'+name+'/?hl=zh-tw'
            print(url)
            print(channel)
            r = requests.get(url, headers=headers, cookies=cookies1)
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
            full_name = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
            for info in jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
                post = info['node']
                post_id = post['id']
                img = post['thumbnail_src']
                try:
                    post_text = post['edge_media_to_caption']['edges'][0]['node']['text']
                    # print(post_text)
                except IndexError:
                    post_text = ' '
                link = 'https://www.instagram.com/p/' + post['shortcode']
                if post_id not in id_list:
                    embed = discord.Embed(title=full_name, url=link,
                                          description=post_text,
                                          color=0xd327a5)
                    embed.set_image(url=img)
                    requests.get('https://docs.google.com/forms/u/0/d/e/1FAIpQLSeK6MTUl4pYTFQBcEfO631scZDgpwc0YHZ-1NtQ8gYk6YICKg/formResponse?entry.9634692=' + post_id + '&fvv=1&draftResponse=%5Bnull%2Cnull%2C%22-2039842183786340156%22%5D%0D%0A&pageHistory=0&fbzx=-2039842183786340156')
                    # print(post_text)
                    await channel.send(embed=embed)
            story_url = 'https://www.instagram.com/graphql/query/?query_hash=90709b530ea0969f002c86a89b4f2b8d&variables=%7B%22reel_ids%22%3A%5B%22' + reel_id + '%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22%22%2C%22stories_video_dash_manifest%22%3Afalse%7D'
            r = requests.get(story_url, headers=headers, cookies=cookies1).text
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
                                                  # timestamp=datetime.datetime.fromtimestamp(takentime),
                                                  color=0xd327a5)
                            embed.set_footer(text=datetime.datetime.fromtimestamp(takentime))
                            embed.set_image(url=i['display_url'])
                            await channel.send(embed=embed)
                            # pass
                        except KeyError:
                            # pass
                            embed = discord.Embed(title=name,
                                                  description=f'來自{name}限時動態的照片',
                                                  url=i['display_url'],
                                                  # timestamp=datetime.datetime.fromtimestamp(takentime),
                                                  color=0xd327a5)
                            embed.set_footer(text=datetime.datetime.fromtimestamp(takentime))
                            embed.set_image(url=i['display_url'])
                            await channel.send(embed=embed)
                        requests.get('https://docs.google.com/forms/u/0/d/e/1FAIpQLSeK6MTUl4pYTFQBcEfO631scZDgpwc0YHZ-1NtQ8gYk6YICKg/formResponse?entry.9634692=' + story_id + '&fvv=1&draftResponse=%5Bnull%2Cnull%2C%22-2039842183786340156%22%5D%0D%0A&pageHistory=0&fbzx=-2039842183786340156')
            except IndexError:
                pass
            await asyncio.sleep(10)


        await asyncio.sleep(random.randint(7000, 7400))

async def fbpost():
    await bot.wait_until_ready()
    while not bot.is_closed():
        channel = bot.get_channel(763443888601432104)
        record = json.loads(requests.get('https://spreadsheets.google.com/feeds/cells/1OtHAi3p3SWP-LbRZIK3Z5etWyf9DGDsTBlkAKbvafGI/1/public/values?alt=json').text)
        sheet_len = len(record['feed']['entry']) - 1
        # print(record)
        fbid_list = []
        while sheet_len > 1:
            fbid_list.append(record['feed']['entry'][sheet_len]['content']['$t'])
            sheet_len -= 2
        # print(id_list)
        r = requests.get('https://www.facebook.com/ToyplaOfficial').text
        soup = BeautifulSoup(r, 'html.parser')
        # print(soup.prettify())
        root = soup.find_all('div', class_='_5pcp _5lel _2jyu _232_')
        # print(root)
        web = root[len(root) - 1].find('a').get('ajaxify')
        # print(web.get('ajaxify').replace('/ToyplaOfficial', 'https://www.facebook.com/ToyplaOfficial'))
        # print(fbid_list, '\n')
        try:
            postid = web.split('/')
        except AttributeError:
            web = root[len(root) - 1].find('a').get('href')
            postid = web.split('/')
        print(postid)
        postlist = soup.find_all('div', attrs={'data-testid': 'post_message'})
        postmessage = ''
        for i in postlist[1].find_all('p'):
            postmessage += (i.text + '\n')
        try:
            if postid[4] not in fbid_list:
                fbid_list.append(postid[4])
                # print(fbid_list)
                print(web)
                website = 'https://www.facebook.com' + web
                embed = discord.Embed(title='**Toypla 官方facebook 更新**',
                                      description=postmessage,
                                      url=website,
                                      # timestamp=datetime.datetime.fromtimestamp(takentime),
                                      color=0x0b8cef)
                await channel.send(embed=embed)
                requests.get('https://docs.google.com/forms/u/0/d/e/1FAIpQLScPA2GG8zHMjHp10rbGtunxJoUEHiuX3nQ46D0kBuEF2PTF2A/formResponse?entry.1669730449=' + str(postid[4]) + '&fvv=1&draftResponse=%5Bnull%2Cnull%2C"-3048720442502913893"%5D%0D%0A&pageHistory=0&fbzx=-3048720442502913893')
                # await channel.send('**Toypla 官方facebook 更新**\n')
                # await channel.send(website)
        except IndexError:
            if postid[len(postid) - 1] not in fbid_list:
                fbid_list.append(len(postid) - 1)
                # print(fbid_list)
                print(web)
                website = 'https://www.facebook.com' + web
                embed = discord.Embed(title='**Toypla 官方facebook 更新**',
                                      description=postmessage,
                                      url=website,
                                      # timestamp=datetime.datetime.fromtimestamp(takentime),
                                      color=0x0b8cef)
                await channel.send(embed=embed)
                requests.get('https://docs.google.com/forms/u/0/d/e/1FAIpQLScPA2GG8zHMjHp10rbGtunxJoUEHiuX3nQ46D0kBuEF2PTF2A/formResponse?entry.1669730449=' + str(postid[len(postid) - 1]) + '&fvv=1&draftResponse=%5Bnull%2Cnull%2C"-3048720442502913893"%5D%0D%0A&pageHistory=0&fbzx=-3048720442502913893')
                # await channel.send('**Toypla 官方facebook 更新**\n')
                # await channel.send(website)
        await asyncio.sleep(random.randint(250, 350))

@bot.command()
async def 飛(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/763785439344721940/image0.png')

@bot.command()
async def 應援T(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/763791574726475786/image.png')

@bot.command()
async def 蹭(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/763804575298748436/921628.t.mp4')

@bot.command()
async def 喝(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763620581001134090/764182778258260008/video0.mov')

@bot.command()
async def 結婚(ctx):
    await ctx.send('跟我結婚吧!夢乃漓雪!!')
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/765243410008768542/video0.mp4')

@bot.command()
async def 我也是(ctx):
    await ctx.send('我也是!')
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/765243565889945600/video0.mp4')

@bot.command()
async def 晚安(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/765284304309583932/image0.png')

@bot.command()
async def curry(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/765815358741282816/image0.jpg')

@bot.command()
async def 茶茶(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/766725650203017246/942003.jpg')

@bot.command()
async def 怕(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763784178114101268/768728431185625098/image0.jpg')

kneellist = ['https://cdn.discordapp.com/attachments/763784178114101268/777605793276493875/image0.jpg', 'https://cdn.discordapp.com/attachments/763784583065501696/771375002464944148/122889428_1466864323503867_4819096974817305487_n.jpg']

@bot.command()
async def 跪(ctx):
    await ctx.send(kneellist[random.randint(0,1)])

@bot.command()
async def 帥(ctx):
    await ctx.send('https://streamable.com/7axwpu')

@bot.command()
async def 炒麵(ctx):
    await ctx.send('https://streamable.com/1w7zxg')

@bot.command()
async def 暴打(ctx):
    await ctx.send('https://streamable.com/r38r60')

@bot.command()
async def 爆打(ctx):
    await ctx.send('https://streamable.com/r38r60')

@bot.command()
async def 河恩(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/763443888601432104/777577907051692072/125185375_694788494783910_5376958512906647317_n.jpg')

@bot.command()
async def 下去(ctx):
    await ctx.send(f'{ctx.author.mention}你才下去,你全部都下去!🖕')

@bot.command()
async def 垃圾(ctx):
    await ctx.send(f'{ctx.author.mention}我知道你是垃圾😌')

changelist = ['https://cdn.discordapp.com/attachments/763784178114101268/776836613253627934/LINE_capture_626975451.543694.jpg', 'https://cdn.discordapp.com/attachments/763443888601432104/765263987205996584/image.png']

@bot.command()
async def 轉推(ctx):
    await ctx.send(changelist[random.randint(0,1)])

bot.loop.create_task(igstory())
bot.loop.create_task(fbpost())

bot.run('bot_token')
