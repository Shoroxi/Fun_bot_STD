import random
import telebot
import requests

import loadconfig
tg = telebot.TeleBot(loadconfig.__telegramtoken__)


def nep():
        '''NEP'''
        neps = [
            'https://cdn.discordapp.com/attachments/102817255661772800/219530759881359360/community_image_1421846157.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219535598187184128/tumblr_nv25gtvX911ubsb68o1_500.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219535698309545984/tumblr_mpub9tTuZl1rvrw2eo2_r1_500.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219535820430770176/dd9f3cc873f3e13fe098429388fc24242a545a21_hq.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219535828773371904/tumblr_nl62nrrPar1u0bcbmo1_500.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219535828995538944/dUBNqIH.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219535906942615553/b3886374588ec93849e1210449c4561fa699ff0d_hq.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219536353841381376/tumblr_nl9wb2qMFD1u3qei8o1_500.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219536345176080384/tumblr_njhahjh1DB1t0co30o1_500.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219536356223877120/tumblr_njkq53Roep1t0co30o1_500.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219536424121139210/tumblr_oalathnmFC1uskgfro1_400.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219536451807739904/tumblr_nfg22lqmZ31rjwa86o1_500.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219536686529380362/tumblr_o98bm76djb1vv3oz0o1_500.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219537181440475146/tumblr_mya4mdVhDv1rmk3cyo1_500.gif',
            'https://i.imgur.com/4xnJN9x.png',
            'https://i.imgur.com/bunWIWD.jpg']
        msg = f'{random.choice(neps)}'
        # title='NEP NEP NEP')
        return msg


def pat():
        '''?????????????????? ????????-????
        -----------
        ~pat @CrazyCatz
        '''

        gifs = [
                'https://i.imgur.com/Nzxa95W.gif',
                'https://i.imgur.com/VRViMGf.gif',
                'https://i.imgur.com/73dNfOk.gif',
                'https://i.imgur.com/hPR7SOt.gif',
                'https://i.imgur.com/IqGRUu4.gif',
                'https://68.media.tumblr.com/f95f14437809dfec8057b2bd525e6b4a/tumblr_omvkl2SzeK1ql0375o1_500.gif',
                ]

        msg = random.choice(gifs)
        return msg


def anime(message):
    '''???????? ???? AniList.co ??????????
        ????????????:
        -----------
        ~anime Mushishi
        '''

    bot = telebot.TeleBot("5201655115:AAFbPgpEaPMThZCUETrvHZiHjqqnAbx1MoI")

    api = 'https://graphql.anilist.co'
    query = '''
        query ($name: String){
          Media(search: $name, type: ANIME) {
            id
            idMal
            description
            title {
              romaji
              english
            }
            coverImage {
              large
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            synonyms
            format
            status
            episodes
            duration
            nextAiringEpisode {
              episode
            }
            averageScore
            meanScore
            source
            genres
            tags {
              name
            }
            studios(isMain: true) {
              nodes {
                name
              }
            }
            siteUrl
          }
        }
        '''
    variables = {
        'name': message.text
    }

    response = requests.post(api, json={'query': query, 'variables': variables})

    if response.status_code == 200:
                    json = response.json()
                    data = json['data']['Media']
                    text = ""
                    text += 'API provided by AniList.co | ID: {}'.format(str(data['id'])) + "\n"
                    text += data['coverImage']['large'] + "\n"
                    if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                        text += '????????????????: ' + data['title']['romaji'] + "\n"
                    else:
                        text += '????????????????: ' + '{} ({})'.format(data['title']['english'], data['title']['romaji']) + "\n"

                    if data['synonyms'] != []:
                        text += '????????????????: ' + ', '.join(data['synonyms']) + "\n"

                    text += '??????: ' + data['format'].replace('_', ' ').title().replace('Tv', 'TV') + "\n"

                    if data['episodes'] != None:
                        print(data['episodes'])
                        if data['episodes'] > 1:
                            text += '????????????????: ' + '{} ???? {} min'.format(data['episodes'], data['duration']) + "\n"
                        else:
                            text += '????????????????????????: ' + str(data['duration']) + ' min' + "\n"

                    text += '????????????: ' + '{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']) + "\n"

                    if data['episodes'] != None:
                        if data['endDate']['day'] == None:
                            text += '??????????: ' + (data['nextAiringEpisode']['episode'] - 1) + "\n"
                        elif data['episodes'] > 1:
                            text += '??????????: ' + '{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'], data['endDate']['year']) + "\n"

                        text += '????????????: ' + data['status'].replace('_', ' ').title() + "\n"

                    try:
                        text += 'Haupt-Studio' + data['studios']['nodes'][0]['name'] + "\n\n"
                    except IndexError:
                        pass
                    text += '????????????: ' + str(data['averageScore']) + "\n"
                    text += '????????: ' + ', '.join(data['genres']) + "\n\n"
                    tags = ''
                    for tag in data['tags']:
                        tags += tag['name'] + ', '
                    text += '????????: ' + tags[:-2] + "\n\n"
                    try:
                        text += '???????????????????????? ????: ' + data['source'].replace('_', ' ').title() + "\n"
                    except AttributeError:
                        pass

                    text += 'AniList Link' + data['siteUrl'] + "\n"
                    text += 'MyAnimeList Link' + 'https://myanimelist.net/anime/' + str(data['idMal'])

                    tg.send_message(message.chat.id, text)
                    return
    else:
        tg.send_message(message.chat.id, ':x: ???? ?????????????? ?????????? ??????????!')
        return


def manga(message):
        '''???????? ???? AniList.co  ??????????

        ????????????:
        -----------
        ~manga Air Gear
        '''

        api = 'https://graphql.anilist.co'
        query = '''
        query ($name: String){
          Media(search: $name, type: MANGA) {
            id
            idMal
            description
            title {
              romaji
              english
            }
            coverImage {
              large
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            status
            chapters
            volumes
            averageScore
            meanScore
            genres
            tags {
              name
            }
            siteUrl
          }
        }
        '''
        variables = {
            'name': message.text
        }

        response = requests.post(api, json={'query': query, 'variables': variables})

        if response.status_code == 200:
                    json = response.json()
                    data = json['data']['Media']

                    text = ""
                    text += 'API provided by AniList.co | ID: {}'.format(str(data['id'])) + "\n"
                    text += data['coverImage']['large'] + "\n"

                    if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                        text += '????????????????: ' + data['title']['romaji'] + "\n"
                    else:
                        text += '????????????????: ' + '{} ({})'.format(data['title']['english'], data['title']['romaji']) + "\n"
                    # embed.add_field(name='Beschreibung', value=data['description'], inline=False)
                    if data['chapters'] != None:
                        # https://github.com/AniList/ApiV2-GraphQL-Docs/issues/47
                        text += '??????????: ', + data['chapters']  + "\n"
                        text += '??????????: ', + data['volumes']  + "\n"
                    text += '????????????' + '{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']) + "\n"
                    if data['endDate']['day'] != None:
                        text += '??????????: ' + '{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'],
                                                                data['endDate']['year'])  + "\n"
                    text += '????????????: ' + data['status'].replace('_', ' ').title() + "\n"
                    text += '??????????????: ' + str(data['averageScore']) + "\n"
                    text += '??????????: ' + ', '.join(data['genres']) + "\n\n"

                    tags = ''
                    for tag in data['tags']:
                        tags += tag['name'] + ', '
                    text += '????????: ' + (tags[:-2]) + "\n\n"

                    text += 'AniList Link: ' + data['siteUrl'] + "\n"
                    text += 'MyAnimeList Link: ' + 'https://myanimelist.net/anime/' + str(data['idMal']) + "\n"

                    tg.send_message(message.chat.id, text)
                    return
        else:
            tg.send_message(message.chat.id, ':x: ???? ?????????????? ?????????? ??????????!')
            return


def get_text_messages(tg, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Pat":
        tg.send_animation(chat_id, animation=pat())

    elif ms_text == "Nep":
        tg.send_animation(chat_id, animation=nep())

    elif ms_text == "?????????? ??????????":
        tg.send_message(chat_id, '?????????? ???????????????? ??????????:')
        tg.register_next_step_handler(message, anime)

    elif ms_text == "?????????? ??????????":
        tg.send_message(chat_id, '?????????? ???????????????? ??????????:')
        tg.register_next_step_handler(message, manga)
