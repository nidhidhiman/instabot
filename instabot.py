import requests,urllib
from termcolor import colored#requests will allow to send HTTP requests without the need of writing 100s of lines of code.
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#create virtual environment
access_token=''
base_url='https://api.instagram.com/v1/' #url of instagram(global variable)

#1
#The endpoint section here provides us with the information for using the API for different tasks.
def own_info():
    request_url = (base_url + 'users/self/?access_token=%s') % (access_token)
    print colored('GET request url :'+request_url,'magenta')
    user_info = requests.get(request_url).json()
    print user_info

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print colored('username: %s','green') %(user_info['data']['username'])
            print colored('no. of followiers: %s','magenta') %(user_info['data']['counts']['followed_by'])
            print colored('no. of people you are following: %s','magenta') %(user_info['data']['counts']['follows'])
            print colored('no. of postes: %s','magenta') %(user_info['data']['counts']['media'])
        else:
            print 'user does not exist'
    else:
        print 'status code is not 200'

def get_user_id(user_name):
    request_url=(base_url+'users/search?q=%s&access_token=%s')%(user_name,access_token)
    print colored('GET request url:'+request_url,'magenta')
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print'status code is not 200 recived!'
        exit()
#2
def get_user_info(user_name):
  user_id = get_user_id(user_name)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (base_url + 'users/%s?access_token=%s') % (user_id, access_token)
  print colored('GET request url :'+request_url,'magenta')
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      print colored('Username: %s','green') %(user_info['data']['username'])
      print colored('No. of followers: %s','magenta') %(user_info['data']['counts']['followed_by'])
      print colored('No. of people you are following: %s','magenta') %(user_info['data']['counts']['follows'])
      print colored('No. of posts: %s','magenta') %(user_info['data']['counts']['media'])
    else:
      print colored('There is no data for this user!','red')
  else:
    print colored('Status code other than 200 received!','red')

#3
def get_own_post():
    request_url=(base_url+'users/self/media/recent/?access_token=%s')%(access_token)
    print colored('GET request url:'+request_url,'magenta')
    own_media=requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded^_^','magenta')
        else:
            print colored('Post does not exist!','red')
    else:
        print 'Status code other than 200 received!'

#4
def get_user_post(user_name):
    user_id=get_user_id(user_name)
    if user_id==None:
        print colored('User does not exist..','red')
        exit()
    request_url=(base_url+'users/%s/media/recent/?access_token=%s') %(user_id,access_token)
    print colored('GET request url:'+request_url,'magenta')
    user_media=requests.get(request_url).json()
    if user_media['meta']['code']==200:

        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                image_name = user_media['data'][0]['id'] + '.jpeg'
                image_url = user_media['data'][0]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print colored('Your image has been downloaded!','green')
            else:
                print ('Post does not exist!','red')
    else:
        print colored('Status code other than 200','red')

def post_id(user_name):
    user_id=get_user_id(user_name)
    if user_id==None:
        print colored('user does not exist','green')
        exit()
    request_url=(base_url+'users/%s/media/recent/?access_token=%s')%(user_id,access_token)
    print colored('GET request url:'+request_url,'magenta')
    user_media=requests.get(request_url).json()
    if user_media['meta']['code']==200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print colored('There is no recent post','red')
            exit()
    else:
        print colored('Status code other then 200','red')
        exit()

#5
def like_list(user_name):            # Defining the Function ............
    media_id = post_id(user_name)  # Getting post id by passing the username .......
    request_url = base_url + 'media/%s/likes?access_token=%s' % (media_id, access_token)    #    passing the end points and media id along with access token ..
    print colored('GET request url : %s\n', 'magenta') % (request_url)
    like_list = requests.get(request_url).json()

    if like_list['meta']['code'] == 200:  # checking the status code .....
        if len(like_list['data']):
            position = 1
            print colored("List of people who Liked Your Recent post", 'blue')
            for users in like_list['data']:
                if users['username']!= None:
                    print position, colored(users['username'],'green')
                    position = position + 1
                else:
                    print colored('No one had liked Your post!\n', 'red')
        else:
            print colored("User Does not have any post.\n",'red')
    else:
        print colored('Status code other than 200 recieved.\n', 'red')
#6
def like_post(user_name): # this function takes the instagram username as the input and likes the most recent post of that user.
    media_id=post_id(user_name)          #it make a call to get post id functionto get post id to be liked
    request_url=(base_url+'media/%s/likes')%(media_id)
    payload={'access_token':access_token}
    print colored('POST request url:'+request_url,'magenta')
    post_like=requests.post(request_url,payload).json()
    if post_like['meta']['code']==200:
        print 'Likes was Successfully done'
    else:
       print'Your likes was unsuccessful. Please TRY AGAIN'

#7
def comment(user_name):         #     Defining the function ......
    media_id = post_id(user_name)    #   Getting media id by calling the get post id function....
    comment_text = raw_input(colored("Please Write Your comment: ",'blue'))
    payload = {"access_token": access_token, "text" : comment_text}
    request_url = (base_url + 'media/%s/comments') % (media_id)
    print colored('POST request url :'+request_url,'magenta')
    post_comment = requests.post(request_url, payload).json() #   Fetching json data ...
    if post_comment['meta']['code'] == 200:             #      checking status code ......
        print colored("Successfully added a new comment!\n",'green')
    else:
        print colored("Unable to add comment.Please Try again!!\n",'red')

def comment_list(user_name):
    # Defining the Function ............
     media_id = post_id(user_name)  # Getting post id by passing the username .......
     request_url = base_url + 'media/%s/comments?access_token=%s' % (media_id, access_token)  # passing the end points and media id along with access token ..
     print colored('GET request url :'+request_url,'magenta')
     comment_list = requests.get(request_url).json()

     if comment_list['meta']['code'] == 200:  # checking the status code .....
         if len(comment_list['data']):
             position = 1
             print colored("List of people who commented on Your Recent post", 'blue')
             for _ in range(len(comment_list['data'])):
                 if comment_list['data'][position - 1]['text']:

                     print colored(comment_list['data'][position - 1]['from']['username'], 'magenta') + colored(
                            ' said: ', 'magenta') + colored(comment_list['data'][position - 1]['text'],
                                                            'blue')  # Json Parsing ..printing the comments ..
                     position = position + 1
                 else:
                        print colored('No one had commented on Your post!\n', 'red')
         else:
                print colored("There is no Comments on User's Recent post.\n", 'red')
     else:
            print colored('Status code other than 200 recieved.\n', 'red')
#8
def post_comment(user_name):
    media_id=post_id(user_name)
    comment_text=raw_input(colored ("Your comment: ",'blue'))
    payload={'access_token':access_token, "text":comment_text}
    request_url=(base_url+'media/%s/comments')%(media_id)
    print colored('POST request url:'+request_url,'magenta')
    make_comment=requests.post(request_url,payload).json()
    if make_comment['meta']['code']==200:
        print colored('Comment Add successfully','blue')
    else:
        print colored('Unable to add comments. Please TRY AGAIN','red')

#9
def delete_negative_comments(user_name):
    media_id=post_id(user_name)
    request_url=(base_url+'media/%s/comments/?access_token=%s')%(media_id,access_token)
    print colored('GET request url:'+request_url,'magenta')
    comment_info=requests.get(request_url).json()
    if comment_info['meta']['code']==200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print colored('Negative comment:'+comment_text,'red')
                    delete_url = (base_url + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, access_token)
                    print colored('DELETE request url :'+delete_url,'magenta')
                    delete_info = requests.delete(delete_url).json()
                    if delete_info['meta']['code'] == 200:
                        print colored('Comment successfully deleted!\n','blue')
                    else:
                        print colored('Unable to delete comment!','red')
                else:
                    print colored('Positive comment :'+comment_text,'green')
        else:
            print colored('There are no existing comments on the post','red')
    else:
        print colored('Status code other than 200','red')

def start_bot():
    while True:
        print colored('Welcome to InstaBot','cyan')
        print colored(' Menu Option:','yellow')
        print colored('  1. Get your own detail\n','green')
        print colored('  2. Get details of user by username\n','green')
        print colored('  3. Get your own recent post\n','green')
        print colored('  4. Get recent post of user by username\n','green')
        print colored('  5. Get list of people who like the recent post of a user\n','green')
        print colored('  6. Like a recent post of a user\n','green')
        print colored('  7. Get a list of comments\n','green')
        print colored('  8. Make a comment on recent \n','green')
        print colored('  9. Delete negetive comments\n','green')
        print colored('  10. Exit\n\n','green')

        choice=raw_input(colored('Enter your choice: ','blue'))
        if choice=="1":
            own_info()
        elif choice=="2":
            user_name=raw_input('Enter the username of user: ')
            get_user_info(user_name)
        elif choice=="3":
            get_own_post()
        elif choice=="4":
            user_name = raw_input('Enter the username of user: ')
            get_user_post(user_name)
        elif choice=="5":
            user_name = raw_input('Enter the username of user: ')
            like_list(user_name)
        elif choice=="6":
            user_name = raw_input('Enter the username of user: ')
            like_post(user_name)
        elif choice=="7":
            user_name = raw_input('Enter the username of user: ')
            comment_list(user_name)
        elif choice=="8":
            user_name = raw_input('Enter the username of user: ')
            post_comment(user_name)
        elif choice=="9":
            user_name = raw_input('Enter the username of user: ')
            delete_negative_comments(user_name)
        elif choice=="10":
            exit()
        else:
            print 'Wrong Choice'

start_bot()
