![](https://github.com/itsikshteinberger/Lista/blob/master/Lista/Media/logo.png) <br/> 
<p align="center">
    <b>Meet Lista,<br/> Having trouble managing multiple shopping lists with different groups? Lista will help you.</b>
</p>
<br/>

## Prerequisites (For those who are not only interested in production)
- A firebase account
- A twillo acount
- Python 3 and following python libraries:
    - flask
    - twilio
    - secrets
    - firebase_admin

## Installation
A production version will be out soon, however, if you still feel like playing with the code feel free to follow the steps below:<br/>
* clone the code
```bash
git clone https://github.com/itsikshteinberger/Lista
```
* Open a new project in your [firebase account](https://console.firebase.google.com/) with a real-time-database. <br/>
Then go to sesttings > serviceaccounts and click on "Generate new private key" - the new JSON file will be saved in the same folder with the code under the name 'lista-firebase.json'. <br/>The URL of your database appears on the same screen, copy it and put it in the [DataBase.py](https://github.com/itsikshteinberger/Lista/blob/master/Lista/DataBase.py) file (line number 11). 
```python
databaseURL: "Your new DataBaseURL"
```
* For a chatbot we need a server, in the development version I used ngrock free server service, You can find the download link [here](https://ngrok.com/download). 
<br/>Once the zip file is downloaded, extract the exe file and open it, in the command that opens write "ngrock http 5000". 
<br/>After the new screen opens copy the second link - you will need it later.
* Log in to your [twillo](https://console.twilio.com/) account. <br/>
Enter to develop > sms > settings > whatsapp-sandbox and run the bot, past the link you copied in the previous step to the textbox next to 'WHEN A MESSAGE COMES IN' label.
<br/> Click 'save' and run the python code.

<br/>Now after attrition, depression and three pounds of pistachio ice cream - the chat bot is running.
<br/>Some of the steps I brought up earlier are explained [here](https://www.twilio.com/blog/build-a-whatsapp-chatbot-with-python-flask-and-twilio) as well.

## User manual
Although the use of chatbot is quite intuitive - but in any case I find it right to add here some points that may be unclear:
* Lista is a classic girl, you can not access her just like that.
<br/> You will need to send hi / hello / :wave: to her to see your lists in a 'list_index. list_name (list_token)' format. <br/><br/>
![](https://github.com/itsikshteinberger/Lista/blob/master/Lista/Media/screen1.png)<br/><br/>
* Each list has a token (a random eight-character string that the computer automatically creates for each list) - you can share this token with friends to join the list.
<br/>You can watch each list token by typing 'Token list_index'.<br/><br/>
![](https://github.com/itsikshteinberger/Lista/blob/master/Lista/Media/screen2.png)<br/><br/>
* If you want to exit from a list you should know that in case that you are the owner of the list - the entire list will be deleted.
* To see what else you can do - type 'help'.
* For convenience ,the bot does not notice the difference between lowercase and uppercase letters.

<br/>

__Have a fun date with Lista :two_hearts:!__

