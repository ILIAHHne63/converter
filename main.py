import telebot 
import datetime 
import time 
import matplotlib 
matplotlib.use('Agg') 
import matplotlib.pyplot as plt 
import src.Globals as G 
import src.support_func as sf 
import src.dynamic_func as df 
import matplotlib.pyplot as plt 
 
token = '6909903472:AAEY_ToAIcs-87o1N3PPDTBp31lRaVHu8AU' 
client = telebot.TeleBot(token) 
 
@client.message_handler(commands=['help']) 
def get_help(message): 
    """Writes information about Commands""" 
    client.send_message(message.chat.id,"/HELP_exchange_and_dynamic\n" + "/get_exchange_and_dynamic") 


@client.message_handler(commands=['start']) 
def start_message(message): 
    """Writes stat message; Shows menu""" 
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True) 
    item1 = telebot.types.KeyboardButton("HELP") 
    item2 = telebot.types.KeyboardButton("GET_EXCHANGE_AND_DYNAMIC") 
    markup.add(item1, item2) 
    client.send_message(message.chat.id, "if you do not know\n how to use this bot \npress HELP or\n print /help", reply_markup=markup) 
 
 
@client.message_handler(content_types=['text']) 
def get_text(message): 
    """Checking if message text is a command""" 
    new_plot = Plot() 
    if message.text.upper()  == 'GET_EXCHANGE_AND_DYNAMIC': 
        msg = client.send_message(message.chat.id, "Write currency as in example:\n    100.5 USD in RUB") 
        client.register_next_step_handler(msg, new_plot.proc_graph) 
    elif message.text.upper() == 'HELP': 
        client.send_message(message.chat.id, G.help_exchange) 
 
 
class Plot(): 
    def init(self): 
        pass 
 
    def proc_graph(self, message): 
        """Checks if format is correct""" 
        msg_list = message.text.upper().split() 
        if len(msg_list) == 4: 
            types = self.check_type(msg_list) 
            if not (0 in types): 
                self.get_xy_send_graph(msg_list, message) 
            else: 
                self.text_wrong_types(msg_list, types, message) 
        else: 
            self.wrong_format(message) 
 
 
    def check_type(self, msg_list): 
        """Checks if types are correct""" 
        type0 = sf.is_rational(str(msg_list[0])) 
        type1 = sf.check_cur(msg_list[1]) 
        type2 = msg_list[2] == "IN" 
        type3 = sf.check_cur(msg_list[3]) 
        types = [type0, type1, type2, type3] 
        return types 
 
 
    def get_xy_send_graph(self, msg_list, message): 
        """Gets x,y lists for graph""" 
        if msg_list[1] == msg_list[3]: 
            client.send_message(message.chat.id, f"{msg_list[0]} {msg_list[1]} is {msg_list[0]} {msg_list[3]}") 
        else: 
            date = datetime.datetime.now().strftime("%d.%m.%Y") 
            x_list, y_list = df.get_exchange_list([msg_list[1], msg_list[3]], date) 
            print(x_list, y_list) 
            self.send_graph_message(y_list, x_list, msg_list[0], msg_list[3], message) 
 
 
    def text_wrong_types(self, msg_list, types, message): 
        """Writes wrong part og user message""" 
        text_list = msg_list 
        for i in range(3): 
            if not types[i]: 
                text_list[i] = f"<i>{text_list[i]}</i>" 
        string1 = " ".join(text_list) 
        client.send_message(message.chat.id, f"Wrong Format:\n{string1}", parse_mode='HTML') 
        msg = client.send_message(message.chat.id, "Write as in example:\n  100.50 USD in EUR") 
        client.register_next_step_handler(msg, self.proc_graph) 
 
 
    def wrong_format(self, message): 
        """Writes that format is wrong""" 
        client.send_message(message.chat.id, f"Wrong Format:") 
        msg = client.send_message(message.chat.id, "Write as in example:\n  100.50 USD in EUR") 
        client.register_next_step_handler(msg, self.proc_graph) 
 
 
    def create_plot(self, amount, y_list, x_list, currency_to): 
        """Creates a lot using dates and currency exchange""" 
        for i in range(len(y_list)): 
            y_list[i] = round(y_list[i] * float(amount), 2) 
        plt.clf() 
 
        for i in range(1, len(x_list)): 
            if i == 1:
                x_list[i] = " "
            if i % 2 == 0: 
                x_list[i] = "   " * i 
 
        plt.title("Exchange Rate") 
        plt.xlabel("dates", fontsize=8) 
        plt.ylabel(f"{currency_to}") 
        plt.plot(x_list, y_list,'o-r', alpha=1, label="first", lw=5, mec='b', mew=2, ms=10) 
 
        plt.savefig("graph.png") 
        plt.clf() 
        return y_list[-1] 
 
 
 
    def send_graph_message(self, y_list, x_list, amount, curr_to, message): 
        """Sends plot and Converted currency or writes No info""" 
        if y_list == -1 or x_list == -1: 
            client.send_message(message.chat.id, "No info") 
        else: 
            last_date_exchange = self.create_plot(amount, y_list, x_list, curr_to) 
            img = open('graph.png', 'rb') 
            client.send_photo(message.chat.id, img) 
            client.send_message(message.chat.id, str(round(last_date_exchange, 2)) + " " + curr_to) 
 
client.polling(none_stop=True, interval=0)
