import sys
import time
import json
import telepot
from pprint import pprint
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from dbhelper import DBHelper
from pointsmgr import PointsMgr

db = DBHelper()
points = PointsMgr()
TOKEN = "517792218:AAE4xZpbaEhSeI8hvOFY9MRtgJc5IbyfW8w"



#Define bot
TOKEN ="517792218:AAE4xZpbaEhSeI8hvOFY9MRtgJc5IbyfW8w"
bot = telepot.Bot(TOKEN)


#Define Functions Here...
def on_callback_query(msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        message_id = telepot.origin_identifier(msg)
        print 'id:' + str(message_id)

        if query_data != 'cancel':
                try: 
                        points_avail = db.get_total(from_id)[0]

                        if int(query_data)*10 < points_avail:
                                points.redeem(query_data,from_id)
                                msg_txt = 'Points redeemed = ' + str(int(query_data)*10)
                                bot.editMessageText(message_id,msg_txt,reply_markup = None)
                                points.total(from_id)
                        
                        else:
                                msg_txt = 'Insufficient points ):'
                
                                points.total(from_id)
                                bot.editMessageText(message_id,msg_txt,reply_markup = None)

                except Exception as e:
                        print e
                

        else:
                bot.editMessageText(message_id,'Cancelled',reply_markup = None)
                
        
                

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    global owner_id
    owner_id = msg['from']['id']
    print owner_id

    if content_type == 'text':
        if msg['text'] == '/late':
            markup = json.dumps({"one_time_keyboard": True, "force_reply": True})
            sent = bot.sendMessage(chat_id, 'How late was she (In mins)?',reply_markup=markup)
                        
            global outbound_id 
            outbound_id = sent['message_id']
            
        
        elif msg['text'] == '/tally':   
                points.tally(owner_id)
                points.total(owner_id)

        elif msg['text'] == '/reset':   
                db.delete_owner(owner_id)
                bot.sendMessage(chat_id, 'Account reset!')



        elif msg['text'] == '/redeem':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
               InlineKeyboardButton(text='$2', callback_data='2'),
               InlineKeyboardButton(text='$3', callback_data='3'),
               InlineKeyboardButton(text='$4', callback_data='4'),
               InlineKeyboardButton(text='$5', callback_data='5'),
               InlineKeyboardButton(text='Cancel', callback_data='cancel'),
            ]])

            bot.sendMessage(chat_id, 'How many points do you want to redeem? ($1 = 10 pts)', reply_markup=keyboard)

                
            
            
        else:
            try:
               inbound_replyto_id = msg['reply_to_message']['message_id']
               print ("in:" + str(inbound_replyto_id))
               print('out:'+ str(outbound_id))

               if inbound_replyto_id == outbound_id:
                   if msg['text'].isdigit() == True:
                       print ('yay')
                       late_time = msg['text']
                       print(late_time)

                       points.add(late_time,owner_id)
                       points.total(owner_id)
                       
                   else:
                       bot.sendMessage(chat_id, 'Invalid response. Please try again!')

                                        



                    #db.add_point(late_time,owner_id)
                    #points = db.get_points(owner_id)
                    #tally = "\n".join(points)
                    #bot.sendMessage(owner_id, tally)
                
                                        
                
                              
                #print('logic check:')
                #print(outbound_id)
                #print(inbound_replyto_id)


               
            except Exception as e:
                print e
                print(msg['text'])
            


         

            

            
           


#Working code here...
db.setup()
MessageLoop(bot, {'chat': on_chat_message,'callback_query': on_callback_query,}).run_forever(1)
print ('Listening ...')

while 1:
    time.sleep(freq)

