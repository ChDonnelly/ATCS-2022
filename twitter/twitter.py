from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:



    def __init__(self):
        self.logged_in = False
        self.current_user = None
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        valid_login = False
        while not valid_login:
            handle = input("What will your twitter handle be?\n")
            password_1 = input("Enter a password:\n")
            password_2 = input("Re-enter your password:\n")
            if password_1 != password_2:
                print("The passwords don't match. Try again")
            else:
                existing_user = db_session.query(User).where(User.username == handle).first()
                if existing_user:
                    print("That username is already taken. Try again")
                else:
                    new_user = User(handle,password_1)
                    db_session.add(new_user)
                    db_session.commit()
                    self.current_user = new_user
                    self.logged_in = True
                    print("Welcome " + handle)
                    valid_login = True     




            
        

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while not self.logged_in:
            username_check = input("Username: ")
            password_check = input("Password: ")
        
            user = db_session.query(User).where(User.username == username_check).first()
            if user and user.password == password_check:
                self.current_user = user
                print("Welcome " + self.current_user.username)
                self.logged_in = True
            else:
                print("Invalid username or password")
            


        

    
    def logout(self):
        self.logged_in = False
        self.current_user = None

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("1. Login\n2. Register User\n0. Exit")
        user_input = int(input("Please select a Menu Option "))
        if user_input == 1:
            self.login()
            return False
        if user_input == 2:
            self.register_user()
            return False
        if user_input == 0:
            self.logout()
            self.end()
            return True
           




    def follow(self):
        user_input = input("Who would you like to follow?\n")
        following = False
        for follower in self.current_user.following:
            if follower.username == user_input:
                following = True
                print("You already follow " + user_input)
        if not following:
            account_following = db_session.query(User).where(User.username == user_input).first()
            self.current_user.following.append(account_following)
            db_session.commit()
            print("You are now following " + user_input)








    def unfollow(self):
        user_input = input("Who would you like to unfollow?\n")
        following = False
        for follower in self.current_user.following:
            if follower.username == user_input:
                following = True
                self.current_user.following.remove(follower)
                #unfollowed_account = db_session.query(Follower).where(Follower.following_id == self.current_user.username).first()
                #db_session.delete(unfollowed_account)
                print("You no longer follow " + user_input)
    
        if not following:
            print("You don't follow " + user_input)
 
    
    
    def tweet(self):
        tweet_content = input("Create Tweet: ")
        tag_content = input("Enter your tags separated by spaces: ").split()
        new_tweet = Tweet(tweet_content,datetime.now(),self.current_user.username)
        tag_list = []
        print(tag_content)
        for tag_index in range(len(tag_content)):
            print(tag_content[tag_index])
            new_tag = Tag(content = tag_content[tag_index])
            db_session.add(new_tag)
            db_session.commit()
            new_tweet.tags.append(new_tag)
        db_session.add(new_tweet)
        db_session.commit()
   


      


    def view_my_tweets(self):
        user_tweets = db_session.query(Tweet).where(Tweet.username == self.current_user.username)
        self.print_tweets(user_tweets)

    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        feed = db_session.query(Tweet).join(Follower,Tweet.username == Follower.following_id and Follower.follower_id == self.current_user.username).order_by(Tweet.id.desc()).limit(5).all()
        self.print_tweets(feed)

        
    
        


    def search_by_user(self):
        user_input = input("Enter a username: ")
        user_tweets = db_session.query(Tweet).where(Tweet.username == user_input).all()
        if not user_tweets: #CHECK THIS!
            print("There is no user by that name")
        else:
            self.print_tweets(user_tweets)


    def search_by_tag(self):
        user_input = input("Enter a tag: ")
        tweets = db_session.query(Tweet).join(TweetTag,Tweet.id == TweetTag.tweet_id).join(Tag,TweetTag.tag_id == Tag.id).where(Tag.content == user_input).all()
        if not tweets:
            print("There are no tweets with this tag")
        else:
            self.print_tweets(tweets)

        


    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()
        
        print("Welcome to ATCS Twitter!")
        game_over = self.startup()

        while not game_over:
            self.print_menu()
            option = int(input(""))
            if option == 1:
                self.view_feed()     
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
                self.end()
                game_over = True
      
               
