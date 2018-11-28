# Dialogflow Integration with Chatfuel using Python

## How to use?
1. Get your **Agent Project Id** from Dialogflow console.

![Project ID](https://raw.githubusercontent.com/pragnakalp/chatfuel-dialogflow-integrator-using-python/master/images/project_id.png)

2. Download **Service Account Credential file** from GCP.

![Service Account](https://raw.githubusercontent.com/pragnakalp/chatfuel-dialogflow-integrator-using-python/master/images/service_account.png)

3. Enter the file path downloaded above in the app.py file on line number 16.
4. Run your code using Ngrok if you are using this integrator from local machine and copy the Ngrok url.

![Run Ngrok](https://raw.githubusercontent.com/pragnakalp/chatfuel-dialogflow-integrator-using-python/master/images/run_ngrok.png)

![Ngrok](https://raw.githubusercontent.com/pragnakalp/chatfuel-dialogflow-integrator-using-python/master/images/ngrok.png)

5. Go to Chatfuel Dashboard and open your existing chatbot or create a new chatbot.

![Chatfuel Dash](https://raw.githubusercontent.com/pragnakalp/chatfuel-dialogflow-integrator-using-python/master/images/chatfuel_dash.png)

6. Go to the Default Answer block and remove all existing cards and add a new JSON API card. In the JSON API card URL textbox, enter the Ngrok URL.

![Chatfuel](https://raw.githubusercontent.com/pragnakalp/chatfuel-dialogflow-integrator-using-python/master/images/chatfuel_set.png)

7. That's it, now you can test your NLU powered chatbot on messenger.

![Messenger](https://raw.githubusercontent.com/pragnakalp/chatfuel-dialogflow-integrator-using-python/master/images/messenger_test.png)

> Developed by [Pragnakalp Solutions - AI, ML, Chatbots, Python Development, Node JS Solutions](https://pragnakalp.com/)
