import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


# Special class for database management
class DataBase:
    def __init__(self, number):
        cred = credentials.Certificate('lista-firebase.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'Entrer your database URL'
        })

        self.ref = db.reference("/")
        self.number = number  # Phone number

        # Check if there are any lists
        try:
            self.lists = []
            key_lists = list(self.ref.child("Users").child(number).get().keys())

            for key, value in self.ref.child("lists").get().items():
                if key in key_lists:
                    self.lists.append(value['Name'] + " (" + value['Token'] + ")")  # Save every list in 'list_name (list_token)' format

        except:
            self.lists = "You do not currently have lists, select one of the following options:\n1. I want to create a " \
                         "new list.\n2. I want to use a friend's list\n "

    # Prettify the lists array
    def Getlist(self):
        if isinstance(self.lists, list):
            lists_string = "These are your lists:\n"
            for key, list_name in enumerate(self.lists):
                lists_string += str(key + 1) + ". " + list_name + ". \n"

            return lists_string
        else:
            return self.lists

    # Add a new shopping list and append it to the database + lists array
    def Addlist(self, name, token):
        try:
            list_name = "list" + str(int(list(self.ref.child("lists").get().keys())[-1][-1]) + 1)
        except:
            list_name = "list1"

        self.ref.child("Users").child(self.number).child(list_name).set(list_name)
        self.ref.child("lists").child(list_name).set({
            "Name": name,
            "Owner": self.number,
            "Status": "The list was created",
            "Token": token
        })

        if isinstance(self.lists, list):
            self.lists.append(name + " (" + token + ")")
        else:
            self.lists = [name + " (" + token + ")"]

    # Delete a shopping list from the database + lists array
    def Deletelist(self, token):
        for key, value in self.ref.child("lists").get().items():

            if value['Token'].lower() == token.lower() and value['Owner'] == self.number:  # Search for the token + Owner check!
                self.ref.child("lists").child(key).delete()  # Delete from data base

                for user, values in self.ref.child("Users").get().items():  # Delete any connection from any user to this list
                    self.ref.child("Users").child(user).child(key).delete()

                if len(self.lists) > 1:  # Check if now the lists array is empty
                    self.lists.remove(value['Name'] + " (" + value['Token'] + ")")
                else:
                    self.lists = "You do not currently have lists, select one of the following options:\n1. I want to create a " \
                                 "new list.\n2. I want to use a friend's list\n "

                return value['Name'] + " has been successfully deleted"

        # If the list is not found then return an error massage
        return "Something went wrong!\nMake sure you have written the correct token and that you are the owner of the list."

    # Add an ingredient to the shopping list in the database
    def AddIngredient(self, index, Ingredient):
        try:  # Check if the index is illegal
            token = self.lists[index - 1].split('(')[-1][:-1]
        except:
            return "I did not find such a list - it may not exist or it may have been deleted."

        for key, value in self.ref.child("lists").get().items():
            if value['Token'] == token:
                self.ref.child("lists").child(key).child("Ingredients").child(Ingredient).set(Ingredient)
                self.ref.child("lists").child(key).child("Status").set(Ingredient + " added")  # Change list status of list to ingredient added
                return Ingredient + " added successfully to " + self.lists[index - 1].split(' (')[0]

        # If the list is not found then return an error massage
        return "I did not find such a list - it may not exist or it may have been deleted."

    # Remove an ingredient to the shopping list in the database
    def SubIngredient(self, index, Ingredient):
        try:  # Check if the index is illegal
            token = self.lists[index - 1].split('(')[-1][:-1]
        except:
            return "I did not find such a list - it may not exist or it may have been deleted."

        for key, value in self.ref.child("lists").get().items():
            if value['Token'] == token:
                try:   # Check if the ingredient is exist, if it is - than remove it from list
                    if not self.ref.child("lists").child(key).child("Ingredients").child(Ingredient).get():
                        raise Exception("Ingredient is None")
                    self.ref.child("lists").child(key).child("Ingredients").child(Ingredient).delete()
                    self.ref.child("lists").child(key).child("Status").set(Ingredient + " deleted")
                    return Ingredient + " deleted successfully from " + self.lists[index - 1].split(' (')[0]
                except:
                    return "I did not find " + Ingredient + " in " + self.lists[index - 1].split(' (')[0]

        # If the list is not found then return an error massage
        return "I did not find such a list - it may not exist or it may have been deleted."

    # Make a new connection in the database between you and the list with the correct Token
    def EnterToList(self, Token):

        for key, value in self.ref.child("lists").get().items():
            if value['Token'].lower() == Token:
                if value['Name'] + " (" + value['Token'] + ")" in self.lists:  # check if you already in the list
                    return "You're already in the list, stupid!"

                # Add a new connection in the database between you and the list and update the the lists array according to it
                self.ref.child("Users").child(self.number).child(key).set(key)
                if isinstance(self.lists, list):
                    self.lists.append(value['Name'] + " (" + value['Token'] + ")")
                else:
                    self.lists = [value['Name'] + " (" + value['Token'] + ")"]

                return "You have successfully logged in to '" + value['Name'] + "' list"

        # If the list is not found then return an error massage
        return "I could not find a list with your token, please try again"

    # Delete the connection in the database between you and the list
    def SubFromList(self, index):
        try:
            Token = self.lists[index - 1].split('(')[-1][:-1]
        except:
            return "I did not find such a list - it may not exist or it may have been deleted."

        for key, value in self.ref.child("lists").get().items():
            if value['Token'] == Token:
                if value['Owner'] == self.number:  # If you are the owner than all the list deleted
                    self.Deletelist(Token)
                    return "Since you are the owner of the list - the list has also been successfully deleted"
                else:
                    # Delete the connection in the database between you and the list and update the list array according to it
                    self.ref.child("Users").child(self.number).child(key).delete()
                    if len(self.lists) == 1:
                        self.lists = "You do not currently have lists, select one of the following options:\n1. I want to create a " \
                                     "new list.\n2. I want to use a friend's list\n "
                    else:
                        self.lists.remove(value['Name'] + " (" + value['Token'] + ")")

        return "I could not find a list with your token, please try again"

    # Prettify the list details
    def ViewList(self, index):
        try:
            Token = self.lists[index - 1].split('(')[-1][:-1]
        except:
            return "I did not find such a list - it may not exist or it may have been deleted."

        for key, value in self.ref.child("lists").get().items():
            if value['Token'] == Token:
                try:
                    Ingredients = '\n'.join(self.ref.child("lists").child(key).child("Ingredients").get())
                    return "*'{}' list owned by {}:* \n\nIngredients: \n{} \n\n Status: {}".format(value['Name'],
                                                                                                   value['Owner'],
                                                                                                   Ingredients,
                                                                                                   value['Status'])
                except:
                    return "*'{}' list owned by {}:* \n\nThere are no any ingredients yet. \n\nStatus: {}".format(value['Name'],
                                                                                                                 value['Owner'],
                                                                                                                 value['Status'])

    # Return the token of an existing list
    def GetToken(self, index):
        try:
            Token = self.lists[index - 1].split('(')[-1][:-1]
            return Token
        except:
            return "I did not find such a list - it may not exist or it may have been deleted."
