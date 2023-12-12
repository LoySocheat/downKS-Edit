import json
import os
import string
import sys
import time
import ctypes
import os
import platform
from zhon.hanzi import punctuation
import requests
import urllib3

urllib3.disable_warnings()

def request_data(url, id, pcursor, ck, ua):
    headers = {
        'content-type': 'application/json',
        'Cookie': ck,
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Referer': 'https://www.kuaishou.com/profile/' + id,
        'User-Agent': ua
    }
    data = {
        "operationName": "visionProfilePhotoList",
        "variables": {"userId": id, "pcursor": pcursor, "page": "profile"},
        "query": "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"}
    data = json.dumps(data)
    data_json = requests.post(url=url, headers=headers, data=data, timeout=6.05).json()
    return data_json

def replace_chars(chars):
    eg_punctuation = string.punctuation
    ch_punctuation = punctuation
    for item1 in eg_punctuation:
        chars = chars.replace(item1, '')
    for item2 in ch_punctuation:
        chars = chars.replace(item2, '')
    chars = chars.replace(' ', '').replace('\n', '').replace('\xa0', '').replace('\r', '')
    return chars

def get_free_space():
    folder = os.path.abspath(sys.path[0])
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 / 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 / 1024

def save(url, page, ck, ua, selfid):
    except_list = []
    count = 0
    id_list = get_all_ids(url, page, ck, ua, selfid)
    for id in id_list:
        count = count + 1
        print(f'Fetching videos for {count}th follower: {id}...')
        num = 0
        while page != 'no_more':
            time.sleep(1)
            data = request_data(url, id, page, ck, ua)
            next_page_pcursor = data['data']['visionProfilePhotoList']['pcursor']
            page = next_page_pcursor
            print(next_page_pcursor)
            data_list = data['data']['visionProfilePhotoList']['feeds']
            for item in data_list:
                num = num + 1
                video_name = item['photo']['caption']
                video_url = item['photo']['photoUrl']
                author = item['author']['name']
                author = replace_chars(author)
                video_name = replace_chars(video_name)
                path = 'F:/videos/kuaishou11'
                if not os.path.exists(path + '/' + author + '/'):
                    os.makedirs(path + '/' + author + '/')
                filepath = path + '/' + author + '/' + str(num) + '.' + video_name + '.mp4'
                if os.path.exists(filepath):
                    print(f'{num}, {video_name} >>> Already exists!!!')
                    continue
                try:
                    video_content = requests.get(url=video_url, timeout=(3, 7)).content
                except:
                    strss = f'{author}_{num}video_name: {video_url}'
                    except_list.append(strss)
                    continue
                with open(filepath, mode='wb') as f:
                    f.write(video_content)
                print(f'{num}, {video_name} >>> Downloaded!!!')
                free_space = get_free_space()
                if free_space <= 1:
                    break
        page = ''
        print(f'All videos downloaded for {count}th follower: {id}!!!')
    with open('yc_info.txt', 'a') as f:
        f.write(str(except_list))
        print('Exception information saved successfully')
    print(except_list)

def request_follow_data(url, pcursor, ck, ua, selfid):
    headers = {
        'content-type': 'application/json',
        'Cookie': ck,
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Referer': 'https://www.kuaishou.com/profile/' + selfid,
        'User-Agent': ua
    }
    data = {
        'operationName': 'visionProfileUserList',
        'query': 'query visionProfileUserList($pcursor: String, $ftype: Int) {\n  visionProfileUserList(pcursor: '
                 '$pcursor, ftype: $ftype) {\n    result\n    fols {\n      user_name\n      headurl\n      '
                 'user_text\n      isFollowing\n      user_id\n      __typename\n    }\n    hostName\n    pcursor\n   '
                 ' __typename\n  }\n}\n',
        'variables': {'ftype': 1, 'pcursor': pcursor}
    }
    data = json.dumps(data)
    follow_json = requests.post(url=url, headers=headers, data=data).json()
    return follow_json

def get_all_ids(url, page, ck, ua, selfid):
    id_list = []
    num = sign = 0
    while page != 'no_more':
        time.sleep(1)
        follow_data = request_follow_data(url, page, ck, ua, selfid)
        next_pcursor = follow_data['data']['visionProfileUserList']['pcursor']
        page = next_pcursor
        sign = sign + 1
        print(f'Page {sign}: {next_pcursor}')
        fols_list = follow_data['data']['visionProfileUserList']['fols']
        for item in fols_list:
            num = num + 1
            user_name = item['user_name']
            user_id = item['user_id']
            id_list.append(user_id)
            print(f'{num}, {user_name}: {user_id} >>> ID obtained successfully!!!')
    print(id_list)
    return id_list


if __name__ == '__main__':
    link = 'https://www.kuaishou.com/graphql'
    # Pcursor must be empty at the beginning, it is the parameter for pagination
    # selfid is the last part of your account URL, for example, in https://www.kuaishou.com/profile/3xkfgnn9hkacbwc, selfid is 3xkfgnn9hkacbwc
    selfid = '3x7hh7bxbegi7aq'
    pcursor = ''
    # ck ='', Fill in the Cookie value after logging in
    ck ='_did=web_1428325654AD71C6; kpf=PC_WEB; clientid=3; did=web_dfcf4a01dc7c21839a608f5a08fd9767; userId=3850140528; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqAB6FnbQFcUdHhZ1N8g6h1GEw_jjRBaK-HgAn30GYsOU2JMxq4B56OrOe_xTMBKYUUj3WJVugGU0ran5K0lfklH5MqlIzLoAquECQsL24CLOpE6_rI0DOxR8-3a5NJLG0VuHNBJK6VPqz5IyY5CVwiG_7WEY7qeyP6MM17yWK04z1S5Gp5qTLPAVdqjv2WGYlV9Yv1eZ1vITROCfn09EfAbNRoS-1Rj5-IBBNoxoIePYcxZFs4oIiDCqiZ64piiW-piR17AIMLiuwIfnenIPcWgimdJyfnN5igFMAE; kuaishou.server.web_ph=ce440346cb066502950a5eb8086b4da49e05; kpn=KUAISHOU_VISION'
    # ua = '' Fill in User-Agent
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    save(link, pcursor, ck, ua, selfid)
