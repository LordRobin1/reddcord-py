import os
import praw
import random
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def create_reddit():
    reddit = praw.Reddit(client_id = CLIENT_ID,
                         client_secret = CLIENT_SECRET,
                         user_agent = "api for reddit v1",
                         check_for_async = False)
    return reddit

def get_images(r, sub):
    
    postList = []
    
    for submission in r.subreddit(sub).hot():
        if ".jpg" in submission.url or ".png" in submission.url:
            postList.append(submission.url)
        elif ".gif" in submission.url:
            tempurl = submission.url.rsplit("?")[0]
            tempurl = tempurl.replace("preview", "i")
            postList.append(tempurl)
        elif "v.redd.it" in submission.url:
            tempurl = f"https://www.reddit.com{submission.permalink}?utm_source=share&utm_medium=web2x&context=3"
            postList.append(tempurl)
    url = random.choice(postList)        
    return url   
    

def sub_info(r, sub):
    info = r.subreddit(sub)
    title = f"r/{info.display_name}"
    id_card = info.widgets.id_card

    desc =  (f"Subscribers: {info.subscribers} \n" +
             f"Currently online: {id_card.currentlyViewingCount} \n" + 
             f"NSFW: {'yes' if info.over18 else 'no'} \n\n" +                
             f"{id_card.description}")

    return title, desc


def testThisScript():
    reddit = create_reddit()
    print('sub? ', end='')
    sub = input()
    # title, desc = sub_info(reddit, sub)
    # print(title, desc)
    url = get_images(reddit, sub)
    print(url)

#testThisScript()