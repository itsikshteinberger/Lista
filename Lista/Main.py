from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from DataBase import DataBase
import secrets

app = Flask(__name__)

db = None
first_msg = True


def isInt(Str):
    try:
        int(Str)
        return True
    except:
        return False


def generate_token():
    all_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&*+, -.:;<=>?@[]^_{|}~"
    return ''.join(secrets.choice(list(all_chars)) for i in range(8))


@app.route('/lista', methods=['POST'])
def lista():
    global db
    global first_msg

    incoming_msg = request.values.get('Body', '').lower().strip()
    phone_number = request.values.get('WaId')

    resp = MessagingResponse()
    msg = resp.message()

    responsed = False

    if first_msg:
        first_msg = False
        db = DataBase(phone_number)

    if incoming_msg == 'hi' or incoming_msg == 'hello' or incoming_msg == "👋":
        msg.body(
            "Hello, my name is Lista.\nI'm here to organize your shopping lists.\n\n" + db.Getlist() + '\nType \'help\' to see what you can do here')
        responsed = True

    if incoming_msg.split(' ')[0] == 'add' and len(incoming_msg.split(' ')) >= 2:
        list_name = ' '.join(incoming_msg.split(' ')[1:])
        list_token = generate_token()
        db.Addlist(list_name, list_token)
        msg.body(list_name + " added successfully")
        responsed = True

    if incoming_msg.split(' ')[0] == 'remove' and len(incoming_msg.split(' ')) >= 2:
        list_token = ' '.join(incoming_msg.split(' ')[1:])
        msg.body(db.Deletelist(list_token))
        responsed = True

    if len(incoming_msg.split(' + ')) >= 2 and isInt(incoming_msg.split(' + ')[0]):
        list_number = int(incoming_msg.split(' + ')[0])
        msg.body(db.AddIngredient(list_number, incoming_msg.split(' + ')[1]))
        responsed = True

    if len(incoming_msg.split(' - ')) >= 2 and isInt(incoming_msg.split(' - ')[0]):
        list_number = int(incoming_msg.split(' - ')[0])
        msg.body(db.SubIngredient(list_number, incoming_msg.split(' - ')[1]))
        responsed = True

    if incoming_msg.split(' ')[0] == 'enter' and len(incoming_msg.split(' ')) >= 2:
        list_token = ' '.join(incoming_msg.split(' ')[1:])
        msg.body(db.EnterToList(list_token))
        responsed = True

    if incoming_msg.split(' ')[0] == 'exit' and len(incoming_msg.split(' ')) == 2:
        if isInt(incoming_msg.split(' ')[1]):
            index = int(incoming_msg.split(' ')[1])
            msg.body(db.SubFromList(index))
            responsed = True

    if incoming_msg.split(' ')[0] == 'view' and len(incoming_msg.split(' ')) == 2:
        if isInt(incoming_msg.split(' ')[1]):
            index = int(incoming_msg.split(' ')[1])
            msg.body(db.ViewList(index))
            responsed = True

    if incoming_msg.split(' ')[0] == 'token' and len(incoming_msg.split(' ')) == 2:
        if isInt(incoming_msg.split(' ')[1]):
            msg.body(db.GetToken(int(incoming_msg.split(' ')[1])))
            responsed = True

    if incoming_msg == 'help':
        msg.body("'Hi' \ 'Hello' \ '👋' - Displaying the lists next to their indexes.\n\n" + \
                 "'Add' list_name - Add a list you own called list_name.\n\n" + \
                 "'Remove' list_token - Delete the list with the token list_token.\n\n" + \
                 "list_index' + 'some_ingredient - Add some_ingredient to the list with list_index.\n\n" + \
                 "list_index' - 'some_ingredient - Remove some_ingredient from the list with list_index.\n\n" + \
                 "'View' list_index - View list ingredients.\n\n" + \
                 "'Enter' list_token - Puts you as a partner on the list with list_token.\n\n" + \
                 "'Exit' list_index - Remove you from being a partner on the list with list_index.\n\n" + \
                 "'Token' list_index - Gets the token of the list.")
        responsed = True

    if not responsed:
        msg.body("I do not understand, type 'help' to see how I can better understand.")

    return str(resp)


if __name__ == "__main__":
    app.run()
