import requests
from termcolor import colored
access_token='2870641552.1021be5.11f103465fa64646bf973126251a4e33'
base_url='https://api.instagram.com/v1/'
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
def get_user_info(user_name):
  user_id = get_user_id(user_name)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (base_url + 'users/%s?access_token=%s') % (user_id, access_token)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      print 'Username: %s' % (user_info['data']['username'])
      print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
      print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
      print 'There is no data for this user!'
  else:
    print 'Status code other than 200 received!'



def start_bot():
    while True:
        print colored('Welcome to InstaBot','cyan')
        print colored(' Menu Option:','yellow')
        print colored('  1. Get details of user by username\n', 'green')
        print colored('  2. Exit\n\n','green')
        choice = raw_input(colored('Enter your choice: ', 'blue'))
        if choice == "1":
            user_name = raw_input('Enter the username of user: ')
            get_user_info(user_name)
        elif choice == "2":
            exit()
        else:
            print 'Wrong Choice'
start_bot()