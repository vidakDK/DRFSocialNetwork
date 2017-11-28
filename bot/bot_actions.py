import requests
import random
import string
import bot.bot_config as cfg


class BotStuff:
    base_url = "http://127.0.0.1:8000"
    registration_url = "{}/{}/".format(base_url, "register")
    login_url = "{}/{}/".format(base_url, "login")
    users_url = "{}/api/{}/".format(base_url, "users")
    posts_url = "{}/api/{}/".format(base_url, "posts")
    votes_url = "{}/api/{}/".format(base_url, "votes")

    def __init__(self):
        self.counter = 1
        self.users_posts = {}  # dict {email : number_of_posts_user_made}
        self.users_passwords = {}  # dict {email : password}
        self.users_likes = {}  # dict {email : number_of_likes}

        # Current attributes that change with every active user
        self.current_token = None
        self.current_user_email = None
        self.current_user_password = None

    def __register_user(self):
        """Registers the next user with regards to the counter value, and sets the active values to this user"""
        email = "user{}@host.com".format(self.counter)
        password = "stupidbotpassword{}".format(self.counter)
        first_name = "Bot{}".format(self.counter)
        last_name = "Botson{}".format(self.counter)
        payload = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password1": password,
            "password2": password,
        }
        req_type = "POST"
        success, resp = self.__send_request(self.registration_url, req_type, payload)
        if success:
            self.users_posts[email] = 0
            self.users_passwords[email] = password
            self.current_user_email = email
            self.current_user_password = password
            self.current_token = None
        return success, resp

    def __login_user(self, email, password):
        payload = {
            "email": email,
            "password": password,
        }
        req_type = "POST"
        success, resp = self.__send_request(self.login_url, req_type, payload)
        if success:
            self.current_token = resp.json()['token']
            self.current_user_email = email
            self.current_user_password = password
        return success, resp

    def __make_post(self):
        payload = {
            "content": ''.join(random.choice(string.ascii_lowercase) for _ in range(cfg.POST_LENGTH)),
        }
        req_type = "POST"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(self.current_token),
        }
        success, resp = self.__send_request(self.posts_url, req_type, payload, headers)
        return success, resp

    def __make_vote(self, action_type, post_id):
        """action_type=1 for like, 0 for unlike"""
        payload = {
            "post_id": post_id,
            "action_type": action_type
        }
        req_type = "POST"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(self.current_token),
        }
        success, resp = self.__send_request(self.votes_url, req_type, payload, headers)
        return success, resp

    def __get_all_posts(self):
        req_type = "GET"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(self.current_token),
        }
        success, resp = self.__send_request(url=self.posts_url, req_type=req_type, headers=headers)
        return success, resp

    @staticmethod
    def __send_request(url, req_type, data=None, headers=None):
        response = 0
        if req_type == 'POST':
            response = requests.post(url=url, json=data, headers=headers)

        elif req_type == 'GET':
            s = requests.Session()
            response = s.get(url=url, headers=headers, params=data)

        if int(response.status_code) in [200, 201]:
            return True, response
        else:
            return False, response

    def __send_random_number_of_posts(self):
        number_posts = random.randint(1, cfg.MAX_POSTS_PER_USER)
        self.users_posts[self.current_user_email] = number_posts
        for i in range(number_posts):
            success, resp = self.__make_post()
            if not success:
                print("Failed to make post, code={}, resp='{}'".format(resp.status_code, resp.text))
                return False
        return True

    def __bot_signup_and_post(self):
        """Register accounts and make posts"""
        for bot_id in range(cfg.NUMBER_OF_USERS):
            success, resp = self.__register_user()
            if not success:
                print("Failed to register user, code={}, resp='{}'".format(resp.status_code, resp.text))
                return False

            success, resp = self.__login_user(self.current_user_email, self.current_user_password)
            if not success:
                print("Failed to login user, code={}, resp='{}'".format(resp.status_code, resp.text))
                return False

            success = self.__send_random_number_of_posts()
            if not success:
                return False

            self.counter += 1
        return True

    @staticmethod
    def __user_has_a_post_with_zero_likes(posts, owner):
        for post in posts:
            if post['owner'] == owner and post['number_of_likes'] == 0:
                return True
        return False

    def __like_one_random_valid_post(self):
        """Find a post that can be liked and like it!"""
        bot_finished = False
        success, resp = self.__get_all_posts()
        if not success:
            print("Failed to get all posts, code={}, resp='{}'".format(resp.status_code, resp.text))
            return success, bot_finished

        # Find one post to like:
        posts = resp.json()
        post_to_like = None
        for post in posts:
            owner = post['owner']
            if self.__user_has_a_post_with_zero_likes(posts, owner):
                posts_by_owner = [p for p in posts if p['owner'] == owner]
                post_to_like = random.choice(posts_by_owner)
                break

        if post_to_like is None:
            print("There is no post with zero likes so bot is finished.")
            success = True
            bot_finished = True
            return success, bot_finished
        else:
            # Otherwise, we can like the post:
            action_type = 1
            success, resp = self.__make_vote(action_type, post_to_like['id'])
            if not success:
                print("Failed to like post with post_id={}, code={}, resp='{}'".format(
                    post_to_like['id'], resp.status_code, resp.text))
            return success, bot_finished

    def __get_next_user_and_like(self):
        # Get all users that have not reached max number of likes:
        valid_users = {k: v for k, v in self.users_likes.items() if v < cfg.MAX_LIKES_PER_USER}
        if not valid_users:
            bot_finished = True
            success = True
            print("No more users that have not reached max likes, we are done.")
            return success, bot_finished

        # Get valid user that has maximum number of posts:
        current_user_email = max(valid_users, key=lambda key: self.users_posts[key])
        self.__login_user(current_user_email, self.users_passwords[current_user_email])

        # Like posts until we run out of posts or we reach max number of likes per user:
        while self.users_likes[current_user_email] < cfg.MAX_LIKES_PER_USER:
            success, bot_finished = self.__like_one_random_valid_post()
            if not success or bot_finished:
                print("Either failure or bot is finished.")
                return success, bot_finished
            self.users_likes[current_user_email] += 1

        print("Reached max number of likes for the current user (email='{}').".format(current_user_email))
        success = True
        bot_finished = False
        return success, bot_finished

    def __bot_like_activity(self):
        """Do like activity according to set rules"""
        done_flag = False
        success = None

        # Initialize user likes to zero:
        for email in self.users_passwords:
            self.users_likes[email] = 0

        while not done_flag:
            success, bot_finished = self.__get_next_user_and_like()
            if not success or bot_finished:
                done_flag = True

        return success

    def start_bot(self):
        print("Starting bot!")

        success = self.__bot_signup_and_post()
        if not success:
            return False
        print("Finished registering accounts and posting.")

        success = self.__bot_like_activity()
        if not success:
            return False
        print("Finished liking posts. We are done, wooooooooo!!!!!")
        return True


if __name__ == '__main__':
    bot = BotStuff()
    bot.start_bot()




