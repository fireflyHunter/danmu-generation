from crawler.scripts.video_download import download_vid
from crawler.scripts.GetAss import download_danmu


def download(vid):
    download_vid(vid)
    download_danmu(vid)
    
    
download("av25961598")
