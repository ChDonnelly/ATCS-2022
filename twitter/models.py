"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")
    
    tweets = relationship("User",
                          secondary = "Tweet",
                          primaryjoin = "User.username ==Tweet.username")
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def __repr__(self):
        print("@" + self.username)

 
class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

class Tweet(Base):
    __tablename__ = "tweets"

    #Columns
    id = Column("id",TEXT,primary_key = True)
    content = Column("content",TEXT,nullable=False)
    timestamp = Column("timestamp",TEXT,nullable=False)
    username = Column("username",ForeignKey("users.username"))

    tweet_tags = relationship("Tweet",
                              secondary = "tweet_tags",
                              primaryjoin = "Tweet.id == TweetTag.tweet_id",
                              )





    #username = Column("username", TEXT, primary_key=True)
    def __repr__(self):
        #QUESTION: HOW DO i CALL THESE REPR FUNCTIONS? Also, what about the tags here, too?
        print(self.username)
        print(self.content)
        print(self.timestamp)



    # TODO: Complete the class


class Tag(Base):
    # TODO: Complete the class
    __tablename__ = "tags"
    id = Column("id",TEXT,primary_key = True)
    content = Column("content",TEXT,nullable = False)
    
    def __repr__(self):
        print("#" + self.content)


class TweetTag(Base):
    # TODO: Complete the class
    __tablename__ = "tweet_tags"
    #Columns
    id = Column("id",TEXT,primary_key = True)
    tweet_id = Column("tweet_id",ForeignKey("tweets.id"))
    tag_id = Column("tag_id",ForeignKey("tags.id"))

    tags = relationship("TweetTag",
                        secondary= "tags",
                        primaryjoin = "TweetTag.tag_id ==Tag.id")
 

