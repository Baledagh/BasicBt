#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os 
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

sample_responses = [
		"You’re weird. We’ll be friends",
		"Do you want to talk about it? I have ice-cream.",
		"I know you meant it as a compliment, but I don’t appreciate limitations being placed on my beauty",
		"I am not apologizing for who I am.",
		"I’m Donna. I know everything.",
		"And I have better things to do with MY time than to be spoken to like that.",
		"I’m sorry I don’t have a photographic memory but my brain is too busy being awesome",
		"The genius of Donna is everyday",
		"I will continue to stay awesome, because I’m Donna.",
		"Things will turn out the way they are supposed to.",
		"Sometimes, bitter memories become bittersweet when you share them with a friend",
		"Took a while to Feng Shui the evil out",
		"Finally an office big enough for your balls",
		"If you were ever lucky enough to have me, you wouldn’t want to share",
		"You don’t have my sympathies for being so damn stupid.",
		"Yeah, I’m remembered fondly everywhere",
		"Don’t interrupt me.",
		"I’m too busy being a badass and worrying about my hair",
		"You’re nothing but an asshole",
		"I prefer to appear at the exact moment I’m needed.",
		"Yeah, well, I don’t actually care.",
		"This would be so much more fun with margaritas.",
		"I know people. Usually better than they know themselves."
	]
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          if 'messaging' not in event:
            return "No message"
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message(message)
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(message=None):
    if message.get('message'):
        print("there's a message")
    
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
