# flask modules
from flask import Flask, render_template, request, make_response, jsonify
# dialogflow python SDK
import dialogflow_v2 as dialogflow
# requests modulw
import requests
# UUID to generate session ids
import uuid
# JSON
import json
# CSV
import csv
# OS module
import os
# add the credential file to environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<ENTER YOUR CREDENTIAL JSON FILE PATH HERE>"

# Flask app initialization
app = Flask(__name__)

# function to detect intent using text with the help of Dialogflow SDK
# project_id - Id of the Dialogflow Agent
# session_id - Id of the user's session
# language_code - language to be use (default: en)
def detect_intent_texts(project_id, session_id, texts, language_code):
        
    # create a session client
    session_client = dialogflow.SessionsClient()

    # create a session
    session = session_client.session_path(project_id, session_id)        

    # iterate through the input texts usually in the form of a list
    for text in texts:        
        # create the text input object
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

        # create query input object
        query_input = dialogflow.types.QueryInput(text=text_input)

        # call detect_intent function to get the response json (DetectIntentResponse object)
        response = session_client.detect_intent(session=session, query_input=query_input, timeout=20)        

        # store all the fulfillment messages into a list
        responses = response.query_result.fulfillment_messages

        # create a copy for future reuse
        df_response = response
        
        # empty variables for different response
        text_response = [] # for text response
        quick_replies_response = None # for quick replies
        card_response = None # for cards

        # iterate through the fufillment responses    
        for i, response in enumerate(responses):

            # proceed if the response is a facebook response (FACEBOOK platform ID is 1)
            if response.platform == 1:                    
                
                # check if the response is a card response
                if response.card.title != "":   
                    # extract card title                    
                    card_title = response.card.title
                    # extract card buttons
                    card_buttons = response.card.buttons

                    # list to store buttons
                    buttons = []

                    # iterate through card buttons
                    for button in card_buttons:
                        # check if the button is web url button
                        if button.postback:
                            # build and append the web_url button to the buttons list
                            buttons.append({
                                "type": "web_url",
                                "url": button.postback,
                                "title": button.text
                            })
                        # else store the button as a text button
                        else:
                            buttons.append({
                                "type": "text",
                                "title": button.text
                            })
                    
                    # create a card response and store it in the card_response variable
                    # this is a chatfuel format JSON
                    card_response = {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "button",
                                "text": card_title,
                                "buttons": buttons
                            }
                        }
                    }                                                        

                # check if the response is a text response
                if response.text.text is not None:
                    # here we are catching exception to ignore errors                   
                    try:
                        # check if the text in the text response is empty or not
                        if response.text.text[0] != "":                            
                            # append to the text response list                            
                            text_response.append({
                                "text": response.text.text[0]
                            })
                    except:
                        # pass if any error
                        pass
                
                # check if the response is a quick replies repsonse    
                if response.quick_replies is not None:

                    # the quick replies text should not be null or empty
                    if quick_replies_response['text'] != "":             
                        # extract quick replies title       
                        quick_reply_title = response.quick_replies.title
                        # extract quick replies data
                        quick_reply_data = response.quick_replies.quick_replies

                        # a list to store quick replies
                        quick_replies = []

                        # iterate through every quick replies element
                        for qr in quick_reply_data:
                            # append the quick replies to the list
                            quick_replies.append({
                                "title": qr,
                                "block_names": ["Default Answer"]
                            })

                        # build the quick replies JSON
                        quick_replies_response = {
                            "text": quick_reply_title,
                            "quick_replies": quick_replies
                        }                                                                                       

        # a main list to store all the responses
        messages = []        
        
        # check if the card reponse if not none and text is not empty
        if card_response is not None:            
            if card_response['attachment']['payload']['text'] != "":
                # append to the messages list
                messages.append(card_response)
        
        # check if the number of text responses is not zero
        if len(text_response) > 0:
            # iterate through the responses and add to the list
            for text in text_response:
                # append to the  messages list
                messages.append(text)
                
        # check for the quick replies response, it should not be None and text should not be empty
        if quick_replies_response is not None:
            if quick_replies_response['text'] != "":
                # append to the  messages list
                messages.append(quick_replies_response)

        # check if the  number of elements in the main messages list is not 0
        if len(messages) > 0:
            main_response = {
                "messages": messages
            }          
        else:
            # if there are no elements then return the fulfillment_text
            main_response = {
                "messages": [
                    {"text": df_response.query_result.fulfillment_text}
                ]
            }
        
        # return the main JSON response
        return main_response        

# function to get the response from the dialogflow SDK
def get_dialogflow_response(messenger_user_input, messenger_user_id):    
    
    # create an empty session variable
    session_id = ""

    # the sessions.csv file is used to store the user's session so that the context should work properly
    # create a sessions.csv file in the root directory
    # open the file in the read mode
    csvfile = open("sessions.csv", 'r')

    # creating a csv reader object 
    csvreader = csv.reader(csvfile, delimiter=",")                 

    # iterate through the rows in the CSV
    for row in csvreader: 
        # search for an existing user in in CSV, if user already exists use the same session ID
        if row[0] == str(messenger_user_id):            
            session_id = str(row[1])
            # break the loop if found
            break        
    
    # if user is not already in the sessions file
    if session_id == "":                
        # create a session ID
        session_id = str(uuid.uuid4())
        csvfile.close()

        # open the sessions file in append mode
        csvfile = open("sessions.csv", 'a')

        # creating a csv writer object
        csvwriter = csv.writer(csvfile, delimiter=",", lineterminator="\n")
        # add the data to the sessions file
        csvwriter.writerow([str(messenger_user_id), session_id])
    
    # call the detect_intent_texts functions and pass the project ID, session_id, messenger_user_input, 'en-US'
    response = detect_intent_texts('indianrailwayinfo-f4b10', session_id, [messenger_user_input], 'en-US')    
    
    # return response
    return response

# main flask python route
@app.route('/')
def index():
    # messenger user id and messenger user input
    messenger_user_id = request.args.get('messenger user id')
    messenger_user_input = request.args.get('last user freeform input')

    # call the get_dialogflow_response, this will return a chatfuel JSON    
    response = get_dialogflow_response(messenger_user_input, messenger_user_id)

    # return the main chatfuel JSON to
    return make_response(jsonify(response))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 
