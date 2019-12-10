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



###Crawling & Scraping on Steam Functions
######crawling developer names
def crawling_steam_dev_names(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    top_game_names = page_soup.find_all(class_ = 'search_result_row')
    dev_list = []

    for i in top_game_names:
        game_url = i['href']
        game_text = make_request_using_cache_for_scraping(game_url)
        game_soup = BeautifulSoup(game_text,'html.parser')
        try:
            dev = game_soup.find(id = 'developers_list').text
            dev = dev.replace('\r','')
            dev = dev.replace('\t','')
            dev = dev.replace('\n','')
        except:
            dev = None

        dev_list.append(dev)

    return dev_list


######Scraping names
def crawling_steam_names(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    top_game_names = page_soup.find_all(class_ = 'search_result_row')
    name_list = []
    for i in top_game_names:
        name_list.append(i.find(class_='title').text)

    return name_list


######crawling decriptions
def crawling_steam_desc(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    top_game_names = page_soup.find_all(class_ = 'search_result_row')
    desc_list = []
    for i in top_game_names:
        game_url = i['href']
        game_text = make_request_using_cache_for_scraping(game_url)
        game_soup = BeautifulSoup(game_text,'html.parser')
        try:
            desc = game_soup.find(class_ = 'game_description_snippet').text
            desc = desc.replace('\r','')
            desc = desc.replace('\t','')
            desc = desc.replace('\n','')
        except:
            desc = None

        desc_list.append(desc)

    return desc_list

######Scraping url
def crawling_steam_url(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    top_game_names = page_soup.find_all(class_ = 'search_result_row')
    url_list = []
    for i in top_game_names:
        url_list.append(i['href'])

    return url_list




def function1():
    ##All Steam developer list
    steam_dev_list_raw = []
    for i in range(1,7):
        steam_base_url = 'https://store.steampowered.com/search/?filter=topsellers&page='
        steam_url = steam_base_url + str(i)
        for i in crawling_steam_dev_names(steam_url):
            steam_dev_list_raw.append(i)

    steam_dev_list_split = []
    for i in steam_dev_list_raw:
        try:
            ilist = i.split(',')
            for ii in ilist:
                steam_dev_list_split.append(ii)
        except:
            steam_dev_list_split.append(i)

    steam_dev_list_cleared = []
    for i in steam_dev_list_split:
        if i != None:
            if ' (Linux)' in i:
                ii = i.replace(' (Linux)','')
            elif ' (Mac)' in i:
                ii = i.replace(' (Mac)','')
            else:
                ii = i

            if ii[0] == ' ':
                ii=ii[1:]
                if ii[-1] == ' ':
                    ii = ii[:-1]
                else:
                    pass
            elif ii[-1] == ' ':
                ii = ii[:-1]
            else:
                pass

            if ii not in steam_dev_list_cleared:
                steam_dev_list_cleared.append(ii)
            else:
                pass

        else:
            pass

    steam_dev_list = []
    for i in steam_dev_list_cleared:
        try:
            steam_dev_list.append(i.replace(' ','-').lower())
        except:
            steam_dev_list.append(i.lower())
######THIS IS FOR DEVELOPER DATA LIST######







###Get developer data from API
cache_file_name = "API_cache.json"
try:
    cache_file_open = open(cache_file_name, 'r')
    cache_file_content = cache_file_open.read()
    cache_dic = json.loads(cache_file_content)
    cache_file_open.close()
except:
    cache_dic = {}

def params_url_combination(baseurl, params):
    sorted_keys = sorted(params.keys())
    added_url = []
    for i in sorted_keys:
        added_url.append("{}-{}".format(i,params[i]))
    return baseurl + "_" + "_".join(added_url)

def make_request_using_cache(baseurl, params, cache_dic = cache_dic):
    url = params_url_combination(baseurl, params)
    if url in cache_dic:
        print("Getting cached data...")
        return cache_dic[url]

    else:
        print("Making a request for new data")
        resp = requests.get(baseurl, params)
        cache_dic[url] = json.loads(resp.text)
        dumped_json_cache = json.dumps(cache_dic)
        fw = open(cache_file_name,'w')
        fw.write(dumped_json_cache)
        fw.close()
        return cache_dic





def function2():
    ##### FIND ALL GAMES, AVERAGE RATING, GAME COUNT, TOTAL REVIEW NUMBER FOR THOSE GAMES
    API_base_url = 'https://api.rawg.io/api/games'
    dev_game_name_list = []
    dev_avg_rating_list = []
    dev_game_count_list = []
    dev_total_review_list = []

    for i in steam_dev_list:
        params = {}
        params['developers'] = i
        API_result_dic = make_request_using_cache(API_base_url, params)
        dev_game_count = len(API_result_dic['results'])
        dev_game_count_list.append(dev_game_count)
        rating_now = 0
        total_review_now = 0
        for i in API_result_dic['results']:
            try:
                dev_game_name_list.append(i['name'])
                rating_now += i['rating']
                total_review_now += i['reviews_count']
            except:
                dev_game_name_list.append(None)
        try:
            dev_avg_rating = rating_now/dev_game_count
            dev_avg_rating = round(dev_avg_rating,1)
        except:
            dev_avg_rating = 0
        dev_avg_rating_list.append(dev_avg_rating)
        dev_total_review_list.append(total_review_now)





# print('##########avg rating')
# print(dev_avg_rating_list)
# print('##########game count')
# print(dev_game_count_list)
# print('##########total review')
# print(dev_total_review_list)
# print(dev_game_name_list)
#####Find all games developed by developers in Steam

######crawling decriptions again
def crawling_steam_desc_through_search(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    try:
        game_link = page_soup.find(class_ = 'search_result_row')['href']
        game_text = make_request_using_cache_for_scraping(game_link)
        game_soup = BeautifulSoup(game_text,'html.parser')
        try:
            desc = game_soup.find(class_ = 'game_description_snippet').text
            desc = desc.replace('\r','')
            desc = desc.replace('\t','')
            desc = desc.replace('\n','')
        except:
            desc = None
    except:
        desc = None

    return desc
######crawling developer names again
def crawling_steam_dev_names_through_search(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    try:
        game_link = page_soup.find_all(class_ = 'search_result_row')['href']
        game_text = make_request_using_cache_for_scraping(game_link)
        game_soup = BeautifulSoup(game_text,'html.parser')
        try:
            dev = game_soup.find(id = 'developers_list').text
            dev = dev.replace('\r','')
            dev = dev.replace('\t','')
            dev = dev.replace('\n','')
        except:
            dev = None
    except:
        dev = None

    return dev

###crawling urls again
def crawling_steam_dev_urls_through_search(url):
    page_text = make_request_using_cache_for_scraping(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    try:
        game_link = page_soup.find_all(class_ = 'search_result_row')['href']
    except:
        game_link = None
    return game_link


def function3():
    desc_2nd_list = []
    dev_2nd_list = []
    url_2nd_list = []
    for i in dev_game_name_list:
        steam_search_url_start = 'https://store.steampowered.com/search/?term='
        steam_search_url = steam_search_url_start + i
        # print(steam_search_url)
        desc_result = crawling_steam_desc_through_search(steam_search_url)
        dev_result = crawling_steam_dev_names_through_search(steam_search_url)
        url_result = crawling_steam_dev_urls_through_search(steam_search_url)
        desc_2nd_list.append(desc_result)
        dev_2nd_list.append(dev_result)
        url_2nd_list.append(url_result)





    # steam_search_url_start = 'https://store.steampowered.com/search/?term='
    # steam_search_url = steam_search_url_start + 'Fallout Shelter'
    # page_text = make_request_using_cache_for_scraping(steam_search_url)
    # page_soup = BeautifulSoup(page_text, 'html.parser')
    # game_link = page_soup.find(class_ = 'search_result_row')['href']
    # game_text = make_request_using_cache_for_scraping(game_link)
    # game_soup = BeautifulSoup(game_text,'html.parser')
    # try:
    #     desc = game_soup.find(class_ = 'game_description_snippet').text
    #     desc = desc.replace('\r','')
    #     desc = desc.replace('\t','')
    #     desc = desc.replace('\n','')
    # except:
    #     desc = None







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

    #Drop table
    statement = '''
       DROP TABLE IF EXISTS 'Developers';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Games';
    '''
    cur.execute(statement)

    conn.commit()

    #Create table Games
    create_games_table_sql = '''
            CREATE TABLE IF NOT EXISTS 'Games' (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Game_name TEXT,
                Decriptions TEXT,
                Game_url TEXT,
                Developer_id INTEGER,
                FOREIGN KEY (Developer_id) REFERENCES Developers(Developer_id)
            );
    '''
    try:
        cur.execute(create_games_table_sql)
    except Error as e:
        print(e)
        print(create_games_table_sql)

    conn.commit()

    #Create table Developers
    create_developer_table_sql = '''
            CREATE TABLE IF NOT EXISTS 'Developers' (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Developer_name TEXT,
                Ave_rating REAL,
                Game_count INTEGER,
                Toatl_review INTEGER
            );
    '''
    try:
        cur.execute(create_developer_table_sql)
    except Error as e:
        print(e)
        print(create_developer_table_sql)

    conn.commit()

    # conn.close()


    for n in range(len(steam_dev_list)):
        insertion = (None, steam_dev_list_split[n], dev_avg_rating_list[n],dev_game_count_list[n],dev_total_review_list[n])
        statement = 'INSERT INTO "Developers"'
        statement += 'VALUES(?,?,?,?,?)'
        cur.execute(statement,insertion)

    conn.commit()


    ######CONNECT DEV NAME WITH ID
    steam_dev_list_split_into_list = []
    for i in steam_dev_list_raw:
        try:
            ilist = i.split(',')
            steam_dev_list_split_into_list.append(ilist)
        except:
            steam_dev_list_split_into_list.append(i)

    global steam_top_names_list
    global steam_top_desc_list
    global steam_top_url_list

    steam_top_names_list = []
    steam_top_desc_list = []
    steam_top_url_list = []
    steam_dev_list_split_into_list = steam_dev_list_split_into_list

    for i in range(1,7):
        steam_base_url = 'https://store.steampowered.com/search/?filter=topsellers&page='
        steam_url = steam_base_url + str(i)
        for ii in crawling_steam_names(steam_url):
            steam_top_names_list.append(ii)
        for ii in crawling_steam_desc(steam_url):
            steam_top_desc_list.append(ii)
        for ii in crawling_steam_url(steam_url):
            steam_top_url_list.append(ii)


    dev_id_name_return  = cur.execute('''
        SELECT Id, Developer_name FROM Developers
    ''')
    dev_id_name_dic = {}
    for i in dev_id_name_return:
        dev_id_name_dic[i[1]] = i[0]

    ###BUILD GAMES DATA LIST PART 1
    steam_name_data_list = []
    steam_desc_data_list = []
    steam_url_data_list = []
    steam_dev_id_list = []
    data_count = 0
    for n in range(len(steam_top_names_list)):
        try:
            for i in steam_dev_list_split_into_list[n]:
                steam_name_data_list.append(steam_top_names_list[n])
                steam_desc_data_list.append(steam_top_desc_list[n])
                steam_url_data_list.append(steam_top_url_list[n])
                steam_dev_id_list.append(dev_id_name_dic[i])
                data_count += 1
        except:
            steam_name_data_list.append(steam_top_names_list[n])
            steam_desc_data_list.append(steam_top_desc_list[n])
            steam_url_data_list.append(steam_top_url_list[n])
            steam_dev_id_list.append(dev_id_name_dic[steam_dev_list_split_into_list[0]])
            data_count += 1




    for n in range(data_count):
        insertion = (None, steam_name_data_list[n], steam_desc_data_list[n],steam_url_data_list[n],steam_dev_id_list[n])
        statement = 'INSERT INTO "Games"'
        statement += 'VALUES(?,?,?,?,?)'
        cur.execute(statement,insertion)

    conn.commit()


    #####BUILD GAMES DATA LIST PART 2
    steam_dev_list_split_into_list2 = []
    for i in dev_2nd_list:
        try:
            ilist = i.split(',')
            steam_dev_list_split_into_list2.append(ilist)
        except:
            steam_dev_list_split_into_list2.append(i)


    steam_name_data_list2 = []
    steam_desc_data_list2 = []
    steam_url_data_list2 = []
    steam_dev_id_list2 = []

    # dev_game_name_list
    # desc_2nd_list
    # url_2nd_list
    # dev_2nd_list

    for n in range(len(dev_game_name_list)):
        if steam_dev_list_split_into_list2[n] != None:
            if len(steam_dev_list_split_into_list2[n])>1:
                for i in steam_dev_list_split_into_list2[n]:
                    if i in steam_dev_list_split:
                        steam_name_data_list2.append(dev_game_name_list[n])
                        steam_desc_data_list2.append(desc_2nd_list[n])
                        steam_url_data_list2.append(url_2nd_list[n])
                        steam_dev_id_list2.append(dev_id_name_dic[i])
                    else:
                        pass
            else:
                steam_name_data_list2.append(dev_game_name_list[n])
                steam_desc_data_list2.append(desc_2nd_list[n])
                steam_url_data_list2.append(url_2nd_list[n])
                steam_dev_id_list2.append(dev_id_name_dic[steam_dev_list_split_into_list2[n]])
        else:
            steam_name_data_list2.append(dev_game_name_list[n])
            steam_desc_data_list2.append(desc_2nd_list[n])
            steam_url_data_list2.append(url_2nd_list[n])
            steam_dev_id_list2.append(None)







    for n in range(len(steam_name_data_list2)):
        insertion = (None, steam_name_data_list2[n], steam_desc_data_list2[n],steam_url_data_list2[n],steam_dev_id_list2[n])
        statement = 'INSERT INTO "Games"'
        statement += 'VALUES(?,?,?,?,?)'
        cur.execute(statement,insertion)

    conn.commit()


if __name__=="__main__":
    function1()
    function2()
    function3()
