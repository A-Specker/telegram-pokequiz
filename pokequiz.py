import logging
import csv
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# i mean gens
levelz = ['1']
backside = False
backside_only = False
shiny = False
shiny_only = False
curr_int = 0
curr_name = ''
in_quiz = False

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, Eddy sucks at Pokemon. Try out /help for... you know, help.')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Options are:\n/new\n/tip <pokename(lower)>\n/stop\n/gen 1,2,...,5 (use Komma so seperate, dont do whitespaces)\n/backside <True/False/only>  ')


def echo(update, context):
    """Echo the user message."""
    global in_quiz
    global curr_name
    global curr_int

    print(update.message.from_user)
    # logger.info(curr_name)
    if in_quiz:
        tip = context.args.lower()
        # logger.info(tip)
        # logger.info(tip is curr_name)
        print(tip)
        # print(curr_name)
        # print(str(tip) is str(curr_name))
        if tip is curr_name:
            logger.info('Done')
            update.message.reply_text("Richtig war die Lösung!")
            in_quiz = False
            curr_int = 0
            curr_name = ''


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def tip(update, context):
    global in_quiz
    global curr_name
    global curr_int


    if in_quiz:
        tipper = context.args[0].lower()
        print(curr_name)
        if curr_name.lower() == tipper.lower():
            update.message.reply_text("Richtig, {} war die Lösung!".format(curr_name))
            in_quiz = False
            curr_int = 0

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def stop(update, context):
    global in_quiz
    global curr_name
    global curr_int

    in_quiz = False
    curr_name = ''
    curr_int = 0



def set_gen(update, context):
    global levelz
    logger.info(levelz)

    levelz = update.message.text.replace("/gen ", "").split(",")
    update.message.reply_text(levelz)
    logger.info(levelz)

def set_backside(update, context):
    global backside
    global backside_only
    boolean = update.message.text.replace("/backside ", "")
    if boolean is 'True' or 'true' or '1':
        backside = True
        backside_only = False
    if boolean is 'False' or 'false' or '0':
        backside = False
        backside_only = False
    if boolean is 'Only' or 'only':
        backside = True
        backside_only = True

def set_shiny(update, context):
    global shiny_only
    global shiny
    boolean = update.message.text.replace("/shiny ", "")
    if boolean is 'True' or 'true' or '1':
        shiny = True
        shiny_only = False
    if boolean is 'False' or 'false' or '0':
        shiny = False
        shiny_only = False
    if boolean is 'Only' or 'only':
        shiny = True
        shiny_only = True

def post_quiz(update, context):
    global in_quiz
    global curr_int
    global curr_name
    global levelz
    global shiny
    global shiny_only
    global backside
    global backside_only
    in_quiz = True
    config = get_config()
    gen = 'g' + random.choice(levelz)
    back_path = 'front'
    shiny_path = ''
    # back
    if backside_only:
        if config[gen]['hasBack']:
            back_path='back'
    elif backside:
        if config[gen]['hasBack']:
            if random.random() < .5:
                back_path='back'
    # shiny - TODO

    num = random.randint(int(config[gen]['from']), int (config[gen]['to']))
    curr_int = num
    pokes = import_pokes()
    curr_name = pokes[str(curr_int)]
    sfx = '.png'
    img_path = './imgs/' + gen + '/' + back_path + '/' + str(num) + sfx
    logger.info(img_path)
    context.bot.send_photo(chat_id=update.effective_message.chat_id, photo=open(img_path, 'rb'))

def get_config():
  return {
        "g1": {
            'hasFront': True,
            'hasFrontShiny': False,

            'hasBack': True,
            'hasBackShiny' : False,
            'from': 0,
            'to': 150
        },
        "g2": {
            'hasFront': True,
            'hasFrontShiny': True,

            'hasBack': True,
            'hasBackShiny' : True,
            'from': 151,
            'to': 251
        },
        "g3": {
            'hasFront': True,
            'hasFrontShiny': True,

            'hasBack': False,
            'hasBackShiny': False,
            'from': 252,
            'to': 386
        },
        "g4": {
            'hasFront': True,
            'hasFrontShiny': True,

            'hasBack': True,
            'hasBackShiny': True,
            'from': 387,
            'to': 493
        },
        "g5": {
            'hasFront': True,
            'hasFrontShiny': True,

            'hasBack': True,
            'hasBackShiny': True,
            'from': 494,
            'to': 649
        }
    }

def main():
    updater = Updater("1202974803:AAFLUR55UYG-dn1wUeZqOkoHQfDplF08EE4", use_context=True)
    config = get_config()
    dp = updater.dispatcher



    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("gen", set_gen))
    dp.add_handler(CommandHandler("backside", set_backside))
    dp.add_handler(CommandHandler("shiny", set_shiny))
    dp.add_handler(CommandHandler("new", post_quiz))
    dp.add_handler(CommandHandler("tip", tip))
    dp.add_handler(CommandHandler("stop", stop))






    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

  
    
def import_pokes():
    pokes = []
    dct = {}
    with open('unsorted.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            pokes.append(row)
        for p in pokes:
            dct[p[0]] = p[1]
    return dct

if __name__ == '__main__':
    main()