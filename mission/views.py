import django
django.setup()
from django.shortcuts import render
from django.views import View
from mission.forms import missionForm
from mission.models import Input
import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
from django.core import serializers
from django.db.models import Count
import schedule
import time
from django.http import HttpResponse
import threading
from ratelimit.decorators import ratelimit
from ratelimit.mixins import RatelimitMixin
from django.core.cache import cache
import concurrent.futures
import datetime
from django.utils import timezone







#find the 403 error from ratelimiting again. then fine where it breaks and add if statement to put template there

apikey = os.environ.get('apikey')

#@ratelimit(key="ip", rate="10/h", method=ratelimit.UNSAFE)
class Homeview(RatelimitMixin, View):
    ratelimit_key = "ip"
    # do 200 for developer key
    ratelimit_rate = "5/m"
    ratelimit_method = 'POST'
    ratelimit_block = True

    template_name = 'mission/index.html'
    template_name1 = 'mission/confirmation.html'
    form_class = missionForm



    def get(self, request):
        # i might need to add my if statement here instead
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request,):
        form = self.form_class(request.POST)
        if form.is_valid():

            #text = form.cleaned_data['username']
            username = str(form.cleaned_data['username'])
            region = form.cleaned_data['region']
            api_key = apikey
            item_dict = {}
            all_kills = []
            # Get summoner id using player's name


            url = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + username + "?api_key=" + api_key
            response = requests.get(url)
            if response.status_code == 403:
                return(self.template_name)
            if response.status_code != 200:
                return render(
                    request,
                    self.template_name,
                    {'form': form}
                )
            else:
                json = (requests.get(url)).json()
                summoner_id = json['id']
                account_id = json['accountId']


                url = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(
                    account_id) + "/recent?api_key=" + api_key

                json = (requests.get(url)).json()
                response = requests.get(url)

                if response.status_code != 200:
                    return render(
                        request,
                        self.template_name1,
                        {'form': form}
                    )
                else:
                    gidlist = []
                    for each in json['matches']:
                        if each['champion'] == 202:
                            gidlist.append(str(each['gameId']))
                        else:
                            top_kill = 0
                            item0 = 0
                            item1 = 0
                            item2 = 0
                            item3 = 0
                            item4 = 0
                            item5 = 0
                            item6 = 0


                # get game data with gameID. First match summ ID with player ID in game to get played ID stats
                for each in gidlist:
                    url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + each + "?api_key=" + api_key
                    json = (requests.get(url)).json()
                    response = requests.get(url)
                    if response.status_code != 200:
                        return render(
                            request,
                            self.template_name,
                            {'form': form}
                        )
                    else:
                        participantIdentities = json['participantIdentities']
                        for each in participantIdentities:
                            if each['player']['summonerId'] == summoner_id:
                                participantId = each['participantId']
                        for each in json['participants']:
                            if each['participantId'] == participantId:
                                kills = each['stats']['kills']
                                all_kills.append(kills)
                                items = [each['stats']['item0'], each['stats']['item1'], each['stats']['item2'], each['stats']['item3'],
                                         each['stats']['item4'], each['stats']['item5'], each['stats']['item6']]

                                item_dict[kills] = items

            if all_kills:
                top_kill = max(all_kills)
                items = item_dict[top_kill]
                item0 = str(items[0])
                item1 = str(items[1])
                item2 = str(items[2])
                item3 = str(items[3])
                item4 = str(items[4])
                item5 = str(items[5])
                item6 = str(items[6])

                try:
                    conn = psycopg2.connect(dbname='d7ur51gud392rj', user='jkmohfinqavvgr', host='ec2-54-83-204-6.compute-1.amazonaws.com', password='487b6c75201e640f89840f6e5e6275d1fe549a7a5df015a5c919bab2fa9dc2f4')
                    print('opened success')
                except:
                    print(datetime.now(), 'unable to connect')
                    return
                else:
                    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                # write data to db

                cur.execute('''INSERT INTO mission_input(username, summoner_id, account_id, top_kill, region, item0, item1, item2, item3, item4, item5, item6)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
                username, summoner_id, account_id, top_kill, region, item0, item1, item2, item3, item4, item5,
                item6))

                conn.commit()
                cur.close()
                conn.close()

                # return HttpResponseRedirect('/mission/')
                args = {'form': form, 'username': username, 'account_id': account_id, 'summoner_id': summoner_id,
                        'top_kill': top_kill, 'region': region, }
                #return template saying they have been entered
                return render(request, self.template_name1, args)

            else:
                top_kill = 0
                try:
                    conn = psycopg2.connect(dbname='d7ur51gud392rj', user='jkmohfinqavvgr',host='ec2-54-83-204-6.compute-1.amazonaws.com', password='487b6c75201e640f89840f6e5e6275d1fe549a7a5df015a5c919bab2fa9dc2f4')
                    print('opened success')
                except:
                    print(datetime.now(), 'unable to connect')
                    return
                else:
                    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                    # write data to db

                cur.execute('''INSERT INTO mission_input(username, summoner_id, account_id, top_kill, region, item0, item1, item2, item3, item4, item5, item6)
                                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
                    username, summoner_id, account_id, top_kill, region, item0, item1, item2, item3, item4, item5,
                    item6))

                conn.commit()
                cur.close()
                conn.close()

                # return HttpResponseRedirect('/mission/')
                args = {'form': form, 'username': username, 'account_id': account_id, 'summoner_id': summoner_id,
                        'top_kill': top_kill, 'region': region, }
                return render(request, self.template_name1, args)



                    # open db


        else:
            return render(
                request,
                self.template_name,
                {'form': form}
            )
















# def db_update():
#
#     threading.Timer(3600, db_update).start()
#     username = Input.objects.all().values_list('username', flat=True)
#     region = Input.objects.all().values_list('region', flat=True)
#     summoner_id = Input.objects.all().values_list('summoner_id', flat=True)
#     account_id = Input.objects.all().values_list('account_id', flat=True)
#     api_key = apikey
#
#
#     for summ, acc, region in zip(summoner_id, account_id, region):
#         summoner_id = str(summ)
#         account_id = str(acc)
#         region = str(region)
#         item_dict = {}
#         all_kills = []
#
#         url = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(
#             account_id) + "?endTime=1521401934000&beginTime=1520969934000" + "&api_key=" + api_key
#         json = (requests.get(url)).json()
#         response = requests.get(url)
#
#         if response.status_code != 200:
#             top_kill = 0
#
#         else:
#             gidlist = []
#             for each in json['matches']:
#                 if each['champion'] == 202:
#                     gidlist.append(str(each['gameId']))
#
#                 else:
#                     top_kill = 0
#
#             for each in gidlist:
#                 url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + each + "?api_key=" + api_key
#                 response = requests.get(url)
#
#                 if response.status_code != 200:
#                     top_kill = 0
#
#                 else:
#                     #url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + each + "?api_key=" + api_key
#
#                     json = (requests.get(url)).json()
#                     participantIdentities = json['participantIdentities']
#
#                     for each in participantIdentities:
#                         if each['player']['summonerId'] == int(summoner_id):
#                             participantId = each['participantId']
#                     for each in json['participants']:
#                         if each['participantId'] == participantId:
#                             kills = each['stats']['kills']
#                             all_kills.append(kills)
#                             items = [each['stats']['item0'], each['stats']['item1'], each['stats']['item2'], each['stats']['item3'],
#                                      each['stats']['item4'], each['stats']['item5'], each['stats']['item6']]
#
#                             item_dict[kills] = items
#
#             if all_kills:
#                 top_kill = max(all_kills)
#                 print(top_kill)
#                 items = item_dict[top_kill]
#                 item0 = str(items[0])
#                 item1 = str(items[1])
#                 item2 = str(items[2])
#                 item3 = str(items[3])
#                 item4 = str(items[4])
#                 item5 = str(items[5])
#                 item6 = str(items[6])
#                 update = Input.objects.filter(summoner_id=summoner_id).update(top_kill=top_kill, item0=item0, item1=item1,item2=item2, item3=item3, item4=item4, item5=item5, item6=item6)
#                 print('updated')
#             else:
#                 top_kill = 0
#                 update = Input.objects.filter(summoner_id=summoner_id).update(top_kill=top_kill,)
#                 print('updated')
#
#
#     return ()

# start= time.time()
# #db_update()
# end = time.time()
# print('time to finish:')
# print(end-start)


# class blob():


#     threading.Timer(3600, db_update).start()
#     summoners = Input.objects.all().values_list('account_id','summoner_id','region')
#     summoners = summoners
#
#     def update(x):
#         api_key = apikey
#         account_id =  x[0]
#         summoner_id = x[1]
#         region = x[2]
#         item_dict ={}
#         all_kills = []
#         url = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(
#             account_id) + "?endTime=1521401934000&beginTime=1520969934000" + "&api_key=" + api_key
#         json = (requests.get(url)).json()
#         response = requests.get(url)
#
#         if response.status_code != 200:
#             pass
#
#
#         else:
#             gidlist = []
#             for each in json['matches']:
#                 if each['champion'] == 202:
#                     gidlist.append(str(each['gameId']))
#
#                 else:
#                     pass
#
#         for each in gidlist:
#             url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + each + "?api_key=" + api_key
#             response = requests.get(url)
#             if response.status_code != 200:
#                 pass
#
#             else:
#                 # url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + each + "?api_key=" + api_key
#                 json = (requests.get(url)).json()
#                 participantIdentities = json['participantIdentities']
#                 for each in participantIdentities:
#                     if each['player']['summonerId'] == int(summoner_id):
#                         participantId = each['participantId']
#                 for each in json['participants']:
#                     if each['participantId'] == participantId:
#                         kills = each['stats']['kills']
#                         all_kills.append(kills)
#                         items = [each['stats']['item0'], each['stats']['item1'], each['stats']['item2'],each['stats']['item3'],each['stats']['item4'], each['stats']['item5'], each['stats']['item6']]
#                         item_dict[kills] = items
#
#
#         if all_kills:
#             top_kill = max(all_kills)
#             print(top_kill)
#             items = item_dict[top_kill]
#             item0 = str(items[0])
#             item1 = str(items[1])
#             item2 = str(items[2])
#             item3 = str(items[3])
#             item4 = str(items[4])
#             item5 = str(items[5])
#             item6 = str(items[6])
#             update = Input.objects.filter(summoner_id=summoner_id).update(top_kill=top_kill, item0=item0, item1=item1,
#                                                                           item2=item2, item3=item3, item4=item4,
#                                                                           item5=item5, item6=item6)
#
#         else:
#             pass
#
#
#
#
#         result = x
#         return(result)
#
#     start = time.time()
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         result = executor.map(update, summoners)
#
#     end = time.time()
#     print('time to finish:')
#     print(end-start)
#     print(result)
#
#
#
#
#
# blob()


def highscores(request):
    poop = Input.objects.order_by('-top_kill')[:25]

    names = serializers.serialize('python', poop, fields=('username'))
    kills = serializers.serialize('python', poop, fields=('top_kill'))
    item0 = serializers.serialize('python', poop, fields=('item0'))
    item1 = serializers.serialize('python', poop, fields=('item1'))
    item2 = serializers.serialize('python', poop, fields=('item2'))
    item3 = serializers.serialize('python', poop, fields=('item3'))
    item4 = serializers.serialize('python', poop, fields=('item4'))
    item5 = serializers.serialize('python', poop, fields=('item5'))
    item6 = serializers.serialize('python', poop, fields=('item6'))

    # 'item0': item0

    args = {'kills': kills, 'names': names, 'item0': item0, 'item1': item1, 'item2': item2, 'item3': item3,
            'item4': item4, 'item5': item5, 'item6': item6}

    return render(request, 'mission/highscores.html', args)


def missions(request):
	return render(request, 'mission/missions.html')

def home(request):
	return render(request, 'mission/home.html')


def permission_denied(request):
    response = render_to_response(
        'errors/403.html'
    )

    return HttpResponseNotFound(response.content)


def custom_403(request, exception):
    return render(request, 'mission/403.html', {}, status=403)

def custom_500(request):
    return render(request, 'mission/500.html', {}, status=500)
