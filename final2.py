import requests
import json
from bs4 import BeautifulSoup
import sqlite3 as sqlite


### Cache
CACHE_FNAME = 'steam_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}


###Scraping request
def make_request_using_cache_for_scraping(url):

    if url in CACHE_DICTION:
        # print('Getting cached data...')
        return CACHE_DICTION[url]

    else:
        print('Making a request for new data')
        resp = requests.get(url)
        CACHE_DICTION[url] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[url]

######Scraping names
def crawling_steam_names(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    top_game_names = page_soup.find_all(class_ = 'search_result_row')
    name_list = []
    for i in top_game_names:
        name_list.append(i.find(class_='title').text)

    return name_list

######Scraping url
def crawling_steam_url(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    top_game_names = page_soup.find_all(class_ = 'search_result_row')
    url_list = []
    for i in top_game_names:
        url_list.append(i['href'])

    return url_list

steam_top_names_list = []
steam_top_url_list = []
steam_url = 'https://store.steampowered.com/search/?filter=topsellers'
for ii in crawling_steam_names(steam_url):
    steam_top_names_list.append(ii)
for ii in crawling_steam_url(steam_url):
    steam_top_url_list.append(ii)




sql_file_name = 'data.sqlite'
def create_connection(db_filename):
    conn = None
    try:
        conn = sqlite.connect(db_filename)
        return conn
    except Error as e:
        print(e)

    return conn


conn = create_connection(sql_file_name)
cur = conn.cursor()

top_25_dic = {}
for n in range(25):
    top_25_dic[str(n+1)] = steam_top_names_list[n]


def interactive_prompt():
    print('The pop up shows TOP 25 selling games on Steam')
    import plotly.graph_objects as go

    fig = go.Figure(data=[go.Table(header=dict(values=['Ranking','Game Name', 'Game Url']),
                     cells=dict(values=[list(range(1,26)),steam_top_names_list, steam_top_url_list]))
                         ])
    fig.show()


    user_select_game_num = input('Select one game to see detail information of its developers (please use the ranking number)')

    user_select_game_name = top_25_dic[user_select_game_num]

    dev_id = cur.execute('''SELECT Developer_id FROM Games
    WHERE Game_name=\'''' + user_select_game_name + '''\'''').fetchall()
    # print(dev_id)
    dev_id_cleared = []
    for i in dev_id:
        if i[0] != None:
            dev_id_cleared.append(i[0])
        else:
            pass

    dev_name_list = []
    dev_ave_rating_list = []
    for i in dev_id_cleared:
        dev_result = cur.execute('''SELECT Developer_name,Game_count,Ave_rating FROM Developers
        WHERE Id=\'''' + str(i) + '''\'''').fetchall()
        dev_name_list.append(dev_result[0][0])
        dev_ave_rating_list.append(dev_result[0][2])

    # print(dev_name_list)

    fig = go.Figure([go.Bar(x=dev_name_list, y=dev_ave_rating_list)])
    fig.show()

    fig = go.Figure(data=[go.Table(header=dict(values=['#','Developer Name','Average Rating']),
                     cells=dict(values=[list(range(1,len(dev_name_list)+1)),dev_name_list,dev_ave_rating_list]))
                         ])
    fig.show()




    user_select_dev_num = input('Select one developer to see all games developed by this developer (please use the ranking number)')

    selected_dev_id = cur.execute('''SELECT Id FROM Developers
    WHERE Developer_name=\'''' + dev_name_list[int(user_select_dev_num)-1] + '''\'''').fetchall()[0][0]

    dev_all_games_raw = cur.execute('''SELECT Game_name,Decriptions FROM Games
    WHERE Developer_id=\'''' + str(selected_dev_id) + '''\'''').fetchall()



    game_names_raw = []
    game_desc_raw = []
    for i in dev_all_games_raw:
        game_names_raw.append(i[0])
        game_desc_raw.append(i[1])

    game_names = []
    game_desc = []
    for n in range(len(game_names_raw)):
        if game_names_raw[n] not in game_names:
            game_names.append(game_names_raw[n])
            game_desc.append(game_desc_raw[n])
        else:
            pass

    fig = go.Figure(data=[go.Table(header=dict(values=['#','Game Names','Game Descriptions']),
                     cells=dict(values=[list(range(1,len(game_names)+1)),game_names,game_desc]))
                         ])
    fig.show()

if __name__=="__main__":
    interactive_prompt()
