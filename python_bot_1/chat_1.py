import mysql.connector, logging ,random
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater,ConversationHandler)

# 錯誤處理function
def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a message to the user"""
    logger.error(f"Exception occurred while handling an update: {context.error}")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# 連接mysql
cnx = mysql.connector.connect(user='root', password='mysql0913-4157',
                                    host='localhost',port = '3306',
                                    database='test')

# /start
def start(update: Update, context: CallbackContext) :
    update.message.reply_text('hello, {},我是python學習機器人!'.format(update.message.from_user.first_name))
    chat_id = update.message.chat_id

    keyboard = [
        [InlineKeyboardButton("變數", callback_data='變數')],
        [InlineKeyboardButton("輸入與輸出", callback_data='輸入與輸出')],
        [InlineKeyboardButton("數值資料型態", callback_data='數值資料型態')],
        [InlineKeyboardButton("運算子", callback_data='運算子')],
        [InlineKeyboardButton("string", callback_data='string')],
        [InlineKeyboardButton("if條件判斷", callback_data='if條件判斷')],
        [InlineKeyboardButton("for迴圈", callback_data='for迴圈')],
        [InlineKeyboardButton("while迴圈", callback_data='while迴圈')],
        [InlineKeyboardButton("串列list", callback_data='串列list')],
        [InlineKeyboardButton("字元tuple", callback_data='字元tuple')],
        [InlineKeyboardButton("字典dict", callback_data='字典dict')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('請選擇要學習的python主題：', reply_markup=reply_markup)

# /restart
def restart(update: Update, context: CallbackContext) :
    chat_id = update.message.chat_id
    keyboard = [
        [InlineKeyboardButton("變數", callback_data='變數')],
        [InlineKeyboardButton("輸入與輸出", callback_data='輸入與輸出')],
        [InlineKeyboardButton("數值資料型態", callback_data='數值資料型態')],
        [InlineKeyboardButton("運算子", callback_data='運算子')],
        [InlineKeyboardButton("string", callback_data='string')],
        [InlineKeyboardButton("if條件判斷", callback_data='if條件判斷')],
        [InlineKeyboardButton("for迴圈", callback_data='for迴圈')],
        [InlineKeyboardButton("while迴圈", callback_data='while迴圈')],
        [InlineKeyboardButton("串列list", callback_data='串列list')],
        [InlineKeyboardButton("字元tuple", callback_data='字元tuple')],
        [InlineKeyboardButton("字典dict", callback_data='字典dict')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('請重新選擇要學習的python主題：', reply_markup=reply_markup)
    

def select_topic(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    # 更新
    context.user_data['last_choice'] = query.data
    
    context.user_data['current_question'] = None
    
    query.message.reply_text('{}, 請點選 -> /begin 開始出題'.format(query.data))

bot = Bot(token="6031589341:AAHMPjIrS_qJZHBqYtnrF9D-6_ctlPTyZVQ")
cnx = mysql.connector.connect(user='root', password='mysql0913-4157',
                                    host='localhost',port = '3306',
                                    database='test')


def create_options_keyboard(options):
    return ReplyKeyboardMarkup.from_row([KeyboardButton(option) for option in options], resize_keyboard=True)


def generate_question(update: Update, context: CallbackContext): 
    

        current_topic = context.user_data['last_choice']

        # 連mysql
        cnx = mysql.connector.connect(user='root', password='mysql0913-4157',
                                        host='localhost',port = '3306',
                                        database='test')
        cursor = cnx.cursor()

        # 隨機選問題
        query = "SELECT id, question, code, a, b, c, d, ans, answer FROM `{}` ORDER BY RAND() LIMIT 1".format(current_topic)
        cursor.execute(query)
        question_id, question, code, a, b, c, d, ans, answer = cursor.fetchone()
        
        context.user_data['current_question'] = {
            'id': str(question_id),
            'options': [a, b, c, d],
            'correct_answer': ans,
            'correct_longanswer': answer
        }

        # 傳送問題
        message = "{}\n\n{}\n\n{}\n{}\n{}\n{}\n".format(question,code,a,b,c,d) if code else question
        bot = context.bot
        bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=keyboard)

        
        answer_handler = MessageHandler(Filters.text & ~Filters.command, check_answer)

        
        updater.dispatcher.add_handler(answer_handler)

def begin(update, context):
    
    current_question = generate_question(update,context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=current_question)
    
    context.user_data['current_question'] = current_question
    context.user_data['correct_answer'] = str(eval(current_question))


def check_answer(update: Update, context: CallbackContext):
    
    current_question = context.user_data['current_question']
    
    user_answer = update.message.text.upper()
    if user_answer == "A" or user_answer =="B" or user_answer =="C" or user_answer =="D" :
        if user_answer == current_question['correct_answer']:
            # 答對
            update.message.reply_text('答對了！\n{}'.format(current_question['correct_longanswer']))
            begin(update, context)
        else:
            # 答錯
            update.message.reply_text('答錯了！正確答案是：{}\n{}'.format(current_question['correct_answer'], current_question['correct_longanswer']))
            begin(update, context)
        
        updater.dispatcher.remove_handler(context.user_data['answer_handler'])
        
        current_question = generate_question()
        context.user_data['current_question'] = current_question
        context.user_data['correct_answer'] = str(eval(''.join(current_question['question'])))
         
        context.bot.send_message(chat_id=update.effective_chat.id, text=current_question)
    elif user_answer == "重新選擇題目類型" :
        context.bot.send_message(chat_id=update.effective_chat.id, text="換題目~")
        return restart(update,context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="無法判讀")
        return


def answer_handler(update: Update, context: CallbackContext):
    updater.dispatcher.add_handler(CommandHandler('answer', answer_handler))

# 按鍵
keyboard = ReplyKeyboardMarkup(
[[KeyboardButton('A'), KeyboardButton('B'), KeyboardButton('C'), KeyboardButton('D')] ,[KeyboardButton('重新選擇題目類型'),KeyboardButton('/start')]], 
resize_keyboard=True)
        
updater = Updater('6031589341:AAHMPjIrS_qJZHBqYtnrF9D-6_ctlPTyZVQ',use_context=True)
start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('begin', begin))
updater.dispatcher.add_handler(CommandHandler('answer', check_answer))
updater.dispatcher.add_error_handler(error_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(select_topic))
updater.start_polling()
updater.idle()