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
        login_info = False
        handle, password_1, password_2 = None
        while login_info != True:
            handle = input("What will your twittle handle be?\n")
            password_1 = input("Enter a password:\n")
            password_2 = input("Re-enter your password:\n")

            if password_1 == password_2:
                new_user = db_session.query(User).where(User.username == handle).first() #Check this line!
                if len(new_user) == 0:
                    break
                else:
                    print("That username is already taken. Try again")
            else:
                print("Those passwords don't match. Try again. \n")
        print("Hey Chris, to check handle: " + handle + " " + password_1)
        new_user = User(handle,password_1)
        db_session.add(new_user) #Check this line
        db_session.commit() #Check this line!

            
        

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        user = None
        while self.logged_in == False:
            username_check = input("Username: ")
            password_check = input("Password: ")
            user = db_session.query(User).where(User.username == username_check).first()
            if user == None or user.password != password_check:
                print("Invalid username or password")
            else:
                self.current_user = user
                self.logged_in = True
        print("Welcome" + user.username)

        

    
    def logout(self):
        self.logged_in = False
        self.current_user = None

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        user_input = int(input("Welcome to ATCS Twitter!\n Please select a Menu Option\1. Login\n 2. Register User\n 0. Exit"))
        if user_input == 0:
            #do exit stuff
            pass
        if user_input == 2:
            self.register_user()
        if user_input == 1:
            self.login()
            
      




    def follow(self):
        other_user = input("Who would you like to follow?\n")
        #Check if they follow them
        #get the user
        following_user = False
        for follower in self.current_user.following:
            if follower.username == other_user:
                print("You already follow " + other_user)
                following_user = True
        if following_user == False:
            #Query user database
            user = db_session.query(User).where(User.username == other_user).first()
            self.current_user.following.append(user)




        
            



    def unfollow(self):
        unfollowed_user = input("Who would you like to unfollow?")
        following = False
        for follower in self.current_user.following:
            if follower.username == unfollowed_user:
                following = True
        

        

        

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

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
