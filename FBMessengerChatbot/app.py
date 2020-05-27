from flask import Flask, request
import os
from torch import optim
from train.data_utils import loadPrepareData, trimRareWords
import torch
import torch.nn as nn
from train.model import EncoderRNN, LuongAttnDecoderRNN, device, trainIters, GreedySearchDecoder, evaluateInput
from pymessenger.bot import Bot
import train.config

app = Flask(__name__)
ACCESS_TOKEN = 'EAAlE2KkA5dYBAI6q0sW3hOFsMBGhXpHHVuLK9cQLiwjdvhXjyZC7f0enLVm7mDVe3EPP6hObCCTK4dRTZBOQrqUFyErweY9Pf04ObTaZCJvJOSPYohhoFZBQjHxvVuy7vITHgv4whpZAnfS60pU56I4kdDC1D4vcbuHmgSaZAR92BUI8NIZBEVg'
VERIFY_TOKEN = 'L1ZOlsiRrlBSbs/xFesH6jjkDm1OzJlwEmPa93iBNz4='
bot = Bot(ACCESS_TOKEN)
dataFile = 'data\\train\\movie_lines_new.txt'
save_dir = os.path.join("data", "state")
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)
voc, pairs = loadPrepareData("Facebbook Messenger Chatbot Chatbot", dataFile)
pairs = trimRareWords(voc, pairs)
checkpoint = 'state'


if train.config.LOADFILENAME:
    # If loading on same machine the model was trained on
    checkpoint = torch.load(train.config.LOADFILENAME)
    # If loading a model trained on GPU to CPU
    # checkpoint = torch.load(loadFilename, map_location=torch.device('cpu'))
    encoder_sd = checkpoint['en']
    decoder_sd = checkpoint['de']
    encoder_optimizer_sd = checkpoint['en_opt']
    decoder_optimizer_sd = checkpoint['de_opt']
    embedding_sd = checkpoint['embedding']
    voc.__dict__ = checkpoint['voc_dict']

embedding = nn.Embedding(voc.num_words, train.config.HIDDEN_SIZE)
if train.config.LOADFILENAME:
    embedding.load_state_dict(embedding_sd)
# Initialize encoder & decoder models
encoder = EncoderRNN(train.config.HIDDEN_SIZE, embedding, train.config.ENCODER_N_LAYERS, train.config.DROPOUT)
decoder = LuongAttnDecoderRNN(train.config.ATTN_MODEL, embedding, train.config.HIDDEN_SIZE, voc.num_words,
                              train.config.DECODER_N_LAYERS, train.config.DROPOUT)
if train.config.LOADFILENAME:
    encoder.load_state_dict(encoder_sd)
    decoder.load_state_dict(decoder_sd)
# Use appropriate device
encoder = encoder.to(device)
decoder = decoder.to(device)

encoder.train()
decoder.train()

encoder_optimizer = optim.Adam(encoder.parameters(), lr=train.config.LEARNING_RATE)
decoder_optimizer = optim.Adam(decoder.parameters(), lr=train.config.LEARNING_RATE * train.config.DECODER_LEARNIN_RATIO)
if train.config.LOADFILENAME:
    encoder_optimizer.load_state_dict(encoder_optimizer_sd)
    decoder_optimizer.load_state_dict(decoder_optimizer_sd)

trainIters(voc, pairs, encoder, decoder, encoder_optimizer, decoder_optimizer,
           embedding, save_dir, train.config.N_ITERATION,
           train.config.BATCH_SIZE, train.config.PRINT_EVERY, train.config.SAVE_EVERY, train.config.CLIP,
           train.config.LOADFILENAME, checkpoint, train.config.TEACHER_FORCING_RATIO)

# Set dropout layers to eval mode
encoder.eval()
decoder.eval()

# Initialize search module
searcher = GreedySearchDecoder(encoder, decoder)


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        # response_sent_text = get_message()
                        response = evaluateInput(searcher, voc, message['message'].get('text'))
                        bot.send_text_message(recipient_id, response)
                    # if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        # response_sent_nontext = get_message()
                        i = 0
                        while i < 1:
                            bot.send_text_message(recipient_id, "Interesting! Anything else I could help?")
                            i += 1
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# if __name__ == "__main__":
#     app.run()
