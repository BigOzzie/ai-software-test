"""
Running this file should print out some of the test data created at the end.

It will also create a SQLite db named "blog.db" in the directory in which it is run.
The db file will need to be deleted before this file can be run again.
"""


"""
peewee is a lightweight ORM that I discovered while working on this test
url: http://peewee.readthedocs.io/en/latest/index.html

installation: pip install peewee
"""
from peewee import *
from time import time


#Example of how to use peewee to connect to a MySQL db instead
#db = MySQLDatabase('mysql_db_name', host='localhost', user='admin', password='1234')

db = SqliteDatabase('blog.db')

class BaseModel(Model):
    id = IntegerField(primary_key=True)
    created_at = DateTimeField(default=time)
    updated_at = DateTimeField(default=time)

    """Set up the db in one base parent model to stay DRY"""
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    first_name = CharField(null=True) #null=True allows the field to be optional
    last_name = CharField(null=True)
    phone_number = CharField(null=True)
    email = CharField(null=True)


class BlogPost(BaseModel):
    title = CharField()
    body = TextField()
    author = ForeignKeyField(User, backref='blog_posts') #backref allows us to reference blog posts from a user object


class Comment(BaseModel):
    body = TextField()
    author = ForeignKeyField(User, backref='comments')
    blog_post = ForeignKeyField(BlogPost, backref='comments')


class Subscription(BaseModel):
    """ Track when users 'follow' other users """
    subscriber = ForeignKeyField(User, backref='subscriptions')
    target_user = ForeignKeyField(User, backref='outside_subscriptions')


class Message(BaseModel):
    """ Basic setup for private messages between users """
    title = CharField()
    body = TextField()
    sender = ForeignKeyField(User, backref='outbox')
    recipient = ForeignKeyField(User, backref='inbox')


""" Testing """
db.create_tables([User, BlogPost, Comment, Subscription, Message])

User.create(username="me", password="1234")
me = User.get(User.username == "me") #reload from the db to get id for later foreign keys

User.create(username="someone_else", password="qwerty")
not_me = User.get(username="someone_else")

BlogPost.create(title="Life is great", body="So, so great.", author = me)
my_post = BlogPost.get(title="Life is great")

comment = Comment.create(body="This really resonated with me.", author=not_me, blog_post=my_post)

subscription = Subscription.create(subscriber=not_me, target_user=me)

message = Message.create(title="Thanks", body="Hey thanks for the add.", sender=me, recipient=not_me)


for message in not_me.inbox:
    print(message.body)

for post in me.blog_posts:
    print(post.title + ": " + post.body)

for outside_subscriptions in me.outside_subscriptions:
    print(outside_subscriptions.subscriber.username)