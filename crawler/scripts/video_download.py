
import os
import re
import json
import click
import requests
from contextlib import closing


class bilibili():
    def __init__(self):
        self.infoheaders = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                    }
        self.downheaders = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        'accept': '*/*',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'Referer': 'https://search.bilibili.com/all?keyword='
                    }
    def get(self, url, vid, savepath='./videos'):
        Vurlinfos = self._GetVideoInfos(url)
        self._Download(Vurlinfos, savepath, vid)
    def _Download(self, Vurlinfos, savepath, vid):
        if not os.path.exists(savepath):
            os.mkdir(savepath)
        name = Vurlinfos[1]
        download_url = Vurlinfos[0]
        with closing(requests.get(download_url, headers=self.downheaders, stream=True, verify=False)) as res:
            total_size = int(res.headers['content-length'])
            #compute size in mb
            size = total_size/(1024*1024)
            if res.status_code == 200:
                label = '[FileSize]:%0.2f MB' % (size)
                with click.progressbar(length=total_size, label=label) as progressbar:
                    with open(os.path.join(savepath, str(vid)+'.flv'), "wb") as f:
                        for chunk in res.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                progressbar.update(1024)
            else:
                print('[ERROR]:Connect error...')
    def _GetVideoInfos(self, url):
        
        res = requests.get(url=url, headers=self.infoheaders)
        pattern = '.__playinfo__=(.*)</script><script>window.__INITIAL_STATE__='
        re_result = re.findall(pattern, res.text)[0]
        temp = json.loads(re_result)
        download_url = temp['durl'][0]['url']
        if 'mirrork' in download_url:
            vid = download_url.split('/')[6]
        else:
            vid = download_url.split('/')[7]
            if len(vid) >= 10:
                vid = download_url.split('/')[6]
        Vurlinfos = [download_url, vid]
        return Vurlinfos

def download_vid(vid):
    url = "https://www.bilibili.com/video/{}/".format(vid)
    bilibili().get(url,vid)

if __name__ == '__main__':

    url = "https://www.bilibili.com/video/av25961598/"
    bilibili().get(url)