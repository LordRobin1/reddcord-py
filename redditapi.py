#import asyncio
import os
import asyncpraw
import random
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def create_reddit():
    reddit = asyncpraw.Reddit(client_id = CLIENT_ID,
                         client_secret = CLIENT_SECRET,
                         user_agent = "api for reddit v1",
                         check_for_async = True)
    return reddit

async def get_images(sub):    
    r = create_reddit()
    postList = []
    subreddit = await r.subreddit(sub)
    async for submission in subreddit.hot():
        if ".jpg" in submission.url or ".png" in submission.url:
            postList.append({"type": "image", "url": submission.url, "title": submission.title})
            continue
        if ".gif" in submission.url:
            tempurl = submission.url.rsplit("?")[0]
            tempurl = tempurl.replace("preview", "i")
            postList.append({"type": "gif", "url": tempurl, "title": submission.title})
            continue
        if "v.redd.it" in submission.url:
            tempurl = f"https://www.reddit.com{submission.permalink}?utm_source=share&utm_medium=web2x&context=3"
            postList.append({"type": "video", "url": tempurl, "title": submission.title})
            continue
        if "gallery"in submission.url:
            postList.append({"type": "gallery", "url": submission.url, "title": submission.title})
            continue
        postList.append({"type": "text", "url": submission.url, "name": submission.name, "title": submission.title, "text": submission.selftext})

    submDict = random.choice(postList)
    print (submDict)
    if submDict['type'] == "text":
        submDict['comment'] = ""        
        name = submDict['name'].split('_')[1]
        submission.comment_limit = 1
        submission.comment_sort = 'top'
        submission = await r.submission(name)        
        try:
            comments = submission.comments
            if(comments):
                submDict['comment'] = comments[0].body
                return submDict
        except Exception as e:
            print(e)
    await r.close()
    return submDict 
    

async def sub_info(sub):
    r = create_reddit()
    info = await r.subreddit(sub, fetch=True)
    title = f"r/{info.display_name}"
    widgets = info.widgets
    id_card = await widgets.id_card()

    cvt = id_card.currentlyViewingText
    if cvt != 'online' and cvt != '':
        online = cvt
    else: online = 'online'

    desc =  (f"Subscribers: {id_card.subscribersCount} {id_card.subscribersText}\n" +
             f"Currently {id_card.currentlyViewingCount} {online}\n" + 
             f"NSFW: {'Yes' if info.over18 else 'No'} \n\n" +                
             f"{id_card.description}")
    await r.close()
    
    return title, desc


async def testThisScript():
    print('sub? ', end='')
    sub = input()
    # title, desc = sub_info(reddit, sub)
    # print(title, desc)
    url = await get_images(sub)
    print(url)
    wait = input()
#asyncio.run(testThisScript())