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
    
    tweets = relationship("Tweet")

     #inside the tweet class, where are my user objects
    #looks for foreign key that matches (looks for foreign key var that matches it)



    def __init__(self,username,password):
        self.username = username
        self.password = password
    def __repr__(self):
        return "@ + self.username" 

 
class Follower(Base):
    __tablename__ = "followers"
   
    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

  

class Tweet(Base):
    __tablename__ = "tweets"

    #Columns
    id = Column("id",INTEGER,primary_key = True)
    content = Column("content",TEXT,nullable=False)
    timestamp = Column("timestamp",DATETIME,nullable=False)
    username = Column("username",ForeignKey("users.username"))
    tags = relationship("Tag",secondary="tweettags",back_populates="tweets")
    user = relationship("User",back_populates="tweets")

    def __init__(self,content,timestamp,username):
        self.content = content
        self.timestamp = timestamp
        self.username = username
        
    def __repr__(self):
        tag_content = [tag.__repr__() for tag in self.tags]
        return self.username + "\n" + self.content + "\n" + " ".join(tag_content) + "\n" + self.timestamp.strftime("%m-%d-%Y %H:%M:%S:%f")



       
        


    # TODO: Complete the class


class Tag(Base):
    # TODO: Complete the class
    __tablename__ = "tags"
    id = Column("id",INTEGER,primary_key = True)
    content = Column("content",TEXT,nullable = False)
    
    def __repr__(self):
        return "#" + self.content
    
   

    tweets = relationship("Tweet",secondary="tweettags",back_populates = "tags")
    #tweets = relationship("Tag",secondary = "tweettags",back_populates = "tags")

    def __init__(self,content):
        self.content = content

class TweetTag(Base):
    # TODO: Complete the class
    __tablename__ = "tweettags"
    #Columns
    id = Column("id",INTEGER,primary_key = True)
    tweet_id = Column("tweet_id",ForeignKey("tweets.id"))
    tag_id = Column("tag_id",ForeignKey("tags.id"))

    
 

