import pyttsx3
import speech_recognition as sr
import wikipedia
import wikipediaapi
import webbrowser
import wolframalpha
import os
from io import BytesIO
import re
from IPython.display import Markdown
import textwrap
import smtplib
import random
import requests
from datetime import datetime
import time
import PIL.Image
from bs4 import BeautifulSoup
import google.generativeai as genai

image_dir = "C:\\Users\\SURAJ PANDEY\\Videos\\image"
#genai.configure(api_key="AIzaSyAccMg6J9cA1BgyAEOvrGtLQ9RH7YbGQhc")
genai.configure(api_key="AIzaSyD9X_Ng-YKUqlewpRlC9SzSQ_ZLRo8SzjA")

def to_markdown(text):
    text = text.replace(".", " *")
    return Markdown(textwrap.indent(text, ">", predicate=lambda _: True))
#gemini-pro
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
#def run_conversation():
#    global chat
#    speak("ya WELCOME IN GRAND CHATING CONVERSATION WORLD")
#    while True:
#        user_input = takeCommand()
#        if "retry" in user_input.lower():
#            continue
#        if "exit" in user_input.lower():
#            break
#        user_response = chat.send_message(user_input)
#        model_response = user_response.text
#        print(f"Model:{user_response.text}")
#        #speak(model_response)
#        chat.history.append({"role": "user", "parts": [user_input]})
#        chat.history.append({"role": "model", "parts": [user_response.text]})


#def wishMe():
#    #hour = int(datetime.datetime.now().hour)
#    hour = int(datetime.now().hour)
#    if hour >= 6 and hour < 12:
#        #speak("Good Morning! SIR")
#    elif hour >= 12 and hour < 16:
#        #speak("Good Afternoon SIR")
#    elif hour >= 16 and hour < 22:
#        #speak("Good Evening SIR")
#    else:
#        #speak("Good Night SIR")
#    #speak(
#        "I am ALAXANDER maded A.I VOICE ASSISTANT by SURAJ kumar PANDEY SIR.please tell me how may I help you "
#    )
#
#def wishMe1():
#    #hour = int(datetime.datetime.now().hour)
#    hour = int(datetime.now().hour)
#    if hour >= 6 and hour < 12:
#        #speak("Good Morning!")
#    elif hour >= 12 and hour < 16:
#        #speak("Good Afternoon")
#    elif hour >= 16 and hour < 22:
#        #speak("Good Evening")
#    else:
#        #speak("Good Night")
#    #speak("I am GOING GOING GOING BYE BYE!! ")
#    c = random.randint(0, 2)
#    music1_dir = "C:\\Users\\SURAJ PANDEY\\Music\\byevid"
#    song = os.listdir(music1_dir)
#    print(song)
#    os.startfile(os.path.join(music1_dir, song[c]))

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "retry"
    return query

user_agent = "ALAXANDER(worldforensic@gmail.com)"
language = "en"
wiki_wiki = wikipediaapi.Wikipedia(user_agent, language)

def get_summary(page_title):
    page = wiki_wiki.page(page_title)
    return page.summary

def check_page_exists(page_title):
    page = wiki_wiki.page(page_title)
    return page.exists()

def get_page_url(page_title):
    page = wiki_wiki.page(page_title)
    return page.fullurl
def get_apod(api_key):
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    return data
api_key = 'Fe0znWeGxezbMOen0GUJGu4sEdsV53cYdfBzcieP'

def process_query(query):
    if "nasa" in query.lower():
        try:
            apod_data = get_apod(api_key)
            result = f"Title: {apod_data['title']}\nExplanation: {apod_data['explanation']}"
            #speak(apod_data['title'])
            print(result)
            webbrowser.open(apod_data['url'])
            return result
        except requests.exceptions.HTTPError as e:
            error_message = f"An error occurred while fetching NASA data: {e}"
            print(error_message)
            return error_message
            #speak("An error occurred while fetching NASA data.")
        except Exception as e:
            error_message = f"An error occurred while fetching NASA data: {e}"
            print(error_message)
            return error_message
            #speak("An error occurred while fetching NASA data.")
    else:
        return "No data found for the query."
def yt_search(yt_query):
    form_query=yt_query.replace(' ','+')
    yt_url=f'https://www.youtube.com/results?search_query={form_query}'
    webbrowser.open(yt_url)
    return yt_url
    
def google_scholar(query):
    formatted_query=query.replace(' ','+')
    search_url=f'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={formatted_query}&btnG='
    webbrowser.open(search_url)
    return search_url
    
def map_search(query):
    formatted_query=query.replace(' ','+')
    search_url=f'https://www.google.com/maps/search/{formatted_query}'
    webbrowser.open(search_url)
    return search_url    

def get_image_path(number):
    return os.path.join(image_dir, f"image_{number}.png")


def perform_image_detection(selected_number):
    image_path = get_image_path(selected_number)

    if os.path.exists(image_path):
        img = PIL.Image.open(image_path)
        try:
            #model = genai.GenerativeModel("gemini-pro-vision")
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = "ANALYSIS THIS: Analyze the objects and describe the context in the image. and where its use in medicime and how"
            response = model.generate_content([prompt,img])
            print(response.text)
            return response.text
            #speak(response.text)
        except Exception as e:
            error_message = f"An error occurred while processing the image: {e}"
            print(error_message)
            return error_message
    else:
            error_message = "Image not found."
            print(error_message)
        
        
def image_search(query):
    formatted_query =query.replace(' ','+')
    
    search_url=f'https://www.google.com/search?q={formatted_query}&tbm=isch&ved=2ahUKEwjEr77jvciDAxXnvmMGHbMQC90Q2-cCegQIABAA&oq={formatted_query}&gs_lcp=CgNpbWcQAzINCAAQgAQQigUQQxCxAzINCAAQgAQQigUQQxCxAzINCAAQgAQQigUQQxCxAzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzoICAAQgAQQsQNQpQdY-Rdgxx5oAXAAeAGAAdACiAGTCZIBBzAuNS4wLjGYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABAMABAQ&sclient=img&ei=1CGZZcT1Cef9juMPs6Gs6A0&bih=695&biw=1536&rlz=1C1VDKB_en-GBIN1077IN1077'
    webbrowser.open(search_url)
    return search_url
    image_links=scrape_image_links(search_url)
def scrape_image_links(search_url):
    response=requests.get(search_url)
    soup=BeautifulSoup(response.text, 'html.parser')
    image_links=[a['href'] for a in soup.find_all('a',{'class':'image-link'})]
    return image_links
    
def extract_image_details(image_url,tag_or_class):
    response = requests.get(image_url)
    soup=BeautifulSoup(response.text, 'html.parser')
    image_name=soup.find('your_tag_or_class').text
    return image_name
def generate_content_from_images(image_links,tag_or_class):
    for link in image_links:
        image_name=extract_image_details(link,tag_or_class)
        image_response = requests.get(link)
        image = PIL.Image.open(BytesIO(image_response.content))
        
        model=genai.GenerativeModel('gemini-pro-vision')
        #model=genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(image)
        print(f"Details about image '{image_name}':")
        print(response.text)
        #speak(response.text)
        
def extract_tag_or_class(user_input):
    tag_match=re.search(r'tag:(\w+)',user_input)
    class_match = re.search(r'class:(\w+)',user_input)
    if tag_match:
        return tag_match.group(1)
    elif class_match:
        return class_match.group(1)
    else:
        return None   
    
def select_image_by_name(image_links,target_name):
    if not image_links:
        print("No images found for the given search query.")
        return None
    for link in image_links:
        image_name=extract_image_details(link)
        if target_name.lower() in image_name.lower():
            return link
    print(f"No image found with the name '{target_name}':")
    return None
def fetch_asteroids(start_date, end_date, api_key="Fe0znWeGxezbMOen0GUJGu4sEdsV53cYdfBzcieP"):
    if not start_date or not end_date:
        #speak("Please provide the start and end dates for fetching asteroid data.")
         
        return "Please provide the start and end dates for fetching asteroid data."
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        near_earth_objects = data.get("near_earth_objects", {})
        
        if near_earth_objects:
            asteroid_details = []
            for date, asteroids in near_earth_objects.items():
                #speak(f"On {date}, the following asteroids are expected to approach Earth:")
                print (f"On {date}, the following asteroids are expected to approach Earth:")
                for asteroid in asteroids:
                    name = asteroid.get("name")
                    diameter = asteroid.get("estimated_diameter", {}).get("meters", {}).get("estimated_diameter_max", "unknown")
                    velocity = asteroid.get("close_approach_data", [{}])[0].get("relative_velocity", {}).get("kilometers_per_hour", "unknown")
                    distance = asteroid.get("close_approach_data", [{}])[0].get("miss_distance", {}).get("kilometers", "unknown")
                    
                    #speak(f"Asteroid {name} with an estimated diameter of {diameter} meters is expected to approach Earth at a velocity of {velocity} kilometers per hour from a distance of {distance} kilometers.")
                    details = (f"Asteroid {name} with an estimated diameter of {diameter} meters is expected to approach Earth at a velocity of {velocity} kilometers per hour from a distance of {distance} kilometers.")
                    asteroid_details.append(details)
            return asteroid_details        
        else:
            #speak("No asteroid data found for the given dates.")
           return  "No asteroid data found for the given dates."
    else:
        #speak("An error occurred while fetching asteroid data.")
        return "An error occurred while fetching asteroid data."

def prompt_for_date(date_type):
    while True:
        #speak(f"Please provide the {date_type} date in the format YYYY-MM-DD.")
        print (f"Please provide the {date_type} date in the format YYYY-MM-DD.")
        date = input(f"Enter {date_type} date (YYYY-MM-DD): ")
        try:
            # Validate the date format
            valid_date = datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            #speak("Invalid date format. Please try again.")
            print("Invalid date format. Please try again.")
def get_news(country="in"):
    news_country_codes = {
        "india": "in",
        "usa": "us","united states": "us","america": "us","uk": "gb","united kingdom": "gb","australia": "au","canada": "ca","france": "fr","germany": "de","japan": "jp","china": "cn", "pakistan": "pk","bangladesh": "bd","nepal": "np","bhutan": "bt","maldives": "mv","afghanistan": "af","albania": "al","iran": "ir","iraq": "iq","syria": "sy","turkey": "tr","saudi arabia": "sa","uae": "ae","qatar": "qa","kuwait": "kw","oman": "om","bahrain": "bh","jordan": "jo","lebanon": "lb","israel": "il",
    }
    country_code = news_country_codes.get(country.lower(), "in")
    news_api_key = "f0397453a3ab47a3a50332ab786b8339"
    news_url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={news_api_key}"

    try:
        response = requests.get(news_url)
        news_data = response.json()
        if news_data["status"] == "ok":
            articles = news_data["articles"][:25]
            headlines = [article["title"] for article in articles]
            return headlines
        else:
            #speak("Unable to fetch news at the moment.")
            return "Unable to fetch news at the moment."
    except Exception as e:
        return f"An error occurred while fetching news: {e}"
        #speak("An error occurred while fetching news.")    
        
def get_train_status(train_number, start_day):
    url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"
    headers = {
        "X-RapidAPI-Key": "b2a97dd30emsh94f00a14247a153p15cb2ajsnd8819d6ced32",
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
    }
    
    querystring = {"trainNo": train_number, "startDay": start_day}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response_data = response.json()
        if response.status_code == 200 and response_data["status"]:
            data = response_data["data"]
            train_start_date = data["train_start_date"]
            train_name = data["train_name"]
            title = data["title"]
            new_message = data["new_message"]
            source = data["source"]
            destination = data["destination"]
            
            train_details = (f"Train number {train_number}, the {train_name} started on {train_start_date} from {source} to {destination}. "
                             f"Latest update: {new_message}. Source station: {source}, Destination station: {destination}.")
            return train_details
        else:
            error_message = response_data.get("message", "An error occurred while fetching train status.")
            return error_message
    except Exception as e:
        return f"Error fetching train status: {e}"
             
def extract_digits(text):
    return''.join(re.findall(r'\d+',text)) 
        
def prompt_for_train_status():
    print("Please tell me the train number you want to check.")
    train_number_response = takeCommand().lower()
    train_number = extract_digits(train_number_response)
    
    print("Please tell me for which day you want to check. You can say today, 1 day ago, 2 days ago, 3 days ago, 4 days ago.")
    day_response = takeCommand().lower()
    
    day_mapping = {
        "today": "0", "current day": "0", "1 day ago": "1", "1 day": "1", "one day": "1", 
        "2 days ago": "2", "2 days": "2", "two days": "2", 
        "3 days ago": "3", "3 days": "3", "three days": "3", 
        "4 days ago": "4", "4 days": "4", "four days": "4"
    }
    
    start_day = next((code for phrase, code in day_mapping.items() if phrase in day_response), "0")
    return get_train_status(train_number, start_day)

                
def get_weather(city):
    weather_api_key = "c1fd90b3f1c009b91ebee2f929b181b3"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"

    try:
        response = requests.get(weather_url)
        weather_data = response.json()

        if response.status_code == 200:
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            temp_celsius = temperature - 273.15
            temp_celsius_rounded = round(temp_celsius, 2)
            return f"The weather in {city} is {description} with a temperature of {temp_celsius_rounded}° Celsius."
        else:
            return f"Unable to fetch weather for {city} at the moment."

    except Exception as e:
        return f"An error occurred while fetching weather data: {e}"

def send_email(subject, body, to_email):
    sender_email = "worldforensic@gmail.com"
    sender_password = "dhya zyay xrau ooew"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, to_email, message)

        return "Email sent successfully!!"

    except Exception as e:
        return f"Eroor sending email: {e}"

def fetch_news(country):
    country_codes = {'india': 'IN', 'usa': 'US', 'united states': 'US', 'america': 'US', 'uk': 'GB', 'united kingdom': 'GB', 'australia': 'AU', 'canada': 'CA', 'france': 'FR', 'germany': 'DE', 'japan': 'JP', 'china': 'CN', 'russia': 'RU', 'brazil': 'BR', 'south africa': 'ZA', 'nigeria': 'NG', 'kenya': 'KE', 'egypt': 'EG', 'mexico': 'MX', 'argentina': 'AR', 'spain': 'ES', 'italy': 'IT', 'netherlands': 'NL', 'switzerland': 'CH', 'sweden': 'SE', 'norway': 'NO', 'denmark': 'DK', 'finland': 'FI', 'ireland': 'IE', 'newzealand': 'NZ', 'singapore': 'SG', 'malaysia': 'MY', 'indonesia': 'ID', 'philippines': 'PH', 'vietnam': 'VN', 'thailand': 'TH', 'south korea': 'KR', 'turkey': 'TR', 'saudi arabia': 'SA', 'uae': 'AE', 'qatar': 'QA', 'kuwait': 'KW', 'oman': 'OM', 'bahrain': 'BH', 'jordan': 'JO', 'lebanon': 'LB', 'pakistan': 'PK', 'bangladesh': 'BD', 'sri lanka': 'LK', 'nepal': 'NP', 'bhutan': 'BT', 'maldives': 'MV', 'afghanistan': 'AF', 'albania': 'AL', 'iran': 'IR', 'iraq': 'IQ', 'syria': 'SY'}
    base_url = 'https://news.google.com/home?hl=en-{}&gl={}&ceid={}'
    country_code = country_codes.get(country.lower(),'IN')
    url = base_url.format(country_code, country_code, country_code)
    webbrowser.open(url)
    return url

app_id = "TTGJYL-82236UH42E"
client = wolframalpha.Client(app_id)

def wolfram_alpha_query(user_query):
    try:
        result = client.query(user_query)
        return next(result.results).text if result.results else "No results found."
    except Exception as e:
        return f"Error processing the Wolfram Alpha query: {e}"

        
def about_me():
     return ("I am Alaxander for Everythings, a voice assistant developed by Suraj Kumar Pandey. My purpose is to provide expert guidance, image processing, information retrieval, counseling, task execution, and learning support. People choose me for my unrivaled mathematical problem-solving abilities, comprehensive question assistance, and efficient coding and software development capabilities. I offer versatility across domains, future-ready AI innovation, and personalized user experiences. Additionally, I prioritize ethical and responsible AI practices, ensuring user privacy and data security. With me, users experience seamless integration with workflows, robust knowledge integration, and an interactive learning environment. I am committed to empowering accessibility and inclusion, revolutionizing technological interaction through voice-driven models, and advancing the quality of life for all users.")
     #speak("I am Alaxander for Everythings, a voice assistant developed by Suraj Kumar Pandey. My purpose is to provide expert guidance, image processing, information retrieval, counseling, task execution, and learning support. People choose me for my unrivaled mathematical problem-solving abilities, comprehensive question assistance, and efficient coding and software development capabilities. I offer versatility across domains, future-ready AI innovation, and personalized user experiences. Additionally, I prioritize ethical and responsible AI practices, ensuring user privacy and data security. With me, users experience seamless integration with workflows, robust knowledge integration, and an interactive learning environment. I am committed to empowering accessibility and inclusion, revolutionizing technological interaction through voice-driven models, and advancing the quality of life for all users.")
          
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
                    
def handle_query(query):
        query = query.lower()
        #query = takeCommand.lower()
        user_res = chat.send_message(query)
        model_response = user_res.text
        chat.history.append({"role": "user", "parts": [query]})
        chat.history.append({"role": "model", "parts": [user_res.text]})
        if query:
          user_res = chat.send_message(query)
          model_response = user_res.text
          chat.history.append({"role": "user", "parts": [query]})
          chat.history.append({"role": "model", "parts": [model_response]}) 
        if "image detection" in query:
            match=re.search(r'\b\d+\b',query)
            
            if match:
                selected_number= int(match.group())
                model_response = perform_image_detection(selected_number)
            else:
                model_response = "No number found in the query. Please specify a number for image detection."
                
          
        elif "image search" in query:
            search_query=query.replace("image search","").strip()
            image_search(search_query)
            model_response = "searching image"
        
        elif "youtube music search" in query:
            yt_query=query.replace("youtube music search","").strip()
            yt_search(yt_query)
            model_response = "searching youtube music"
        
        elif "nasa image" in query:
            model_response=process_query(query)
       
        elif "near earth object" in query:
            #speak("Fetching NASA asteroid data...")
            start_date = prompt_for_date("start")
            end_date = prompt_for_date("end")
            model_response = fetch_asteroids(start_date, end_date)           
        elif "update news" in query:
            country = query.replace("update news", "").strip().lower()
            model_response = get_news(country)
        
        elif "nasa" in query:
            get_apod(api_key)
              
        elif "google scholar" in query:
            search_query=query.replace("google scholar","").strip()
            google_scholar(search_query)
            model_response = "searching google scholar"
        
        elif "open news" in query:
            country = query.replace("open news", "").strip().lower()
            fetch_news(country)
            model_response = "searching news"
        
        elif "map search" in query:
            map_query=query.replace("map search","").strip()
            map_search(map_query)
            model_response = "searching map"
        
        elif "weather in" in query:
            city_name = query.split("weather in")[-1].strip()
            model_response = get_weather(city_name)

        elif "train status" in query:
            model_response = prompt_for_train_status()
        elif "tell me about yourself" in query or "about yourself" in query or "who are you" in query:
            model_response = about_me()
        elif "send email" in query:
            try:
               print("what is the subject of the email?")
               subject = takeCommand()
   
               #speak("What is the message of the email?")
               print("What is the message of the email?")
               body = takeCommand()
   
               #speak("What is the username of the recipient's email address?")
               print("What is the username of the recipient's email address?")
               username = takeCommand().replace(" ", "")
   
               #speak("What is the domain of the recipient's email address?")
               print("What is the domain of the recipient's email address?")
               domain = takeCommand().replace(" ", "")
   
               to_email = f"{username}@{domain}"
               send_email(subject, body, to_email)
               model_response = "Email sent successfully!!"
            except Exception as e:
                model_response = f"Error sending email: {e}"
        
        #else:      
        #      print(model_response)
        #      #speak(model_response)
        #      chat.history.append({"role": "user", "parts": [query]})
        #      chat.history.append({"role": "model", "parts": [user_res.text]})

        if "wikipedia" in query.lower():
            #speak("Searching wikipedia...")
            print("Searching wikipedia...")
            query = query.replace("wikipedia", "").strip()

            try:
                results = wikipedia.summary(query, sentences=10)
                #speak("According to wikipedia")
                print("According to wikipedia")
                print(results)
                model_response = results
                #speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                model_response = f"Ambiguous term. Suggestions:{e.options}"
                #speak(f"Ambiguous trm. Suggestions: {', '.join(e.options)}")
            except wikipedia.exceptions.PageError:
                model_response = f"Page for '{query}' not found on wikipedia."
                #speak(f"Sorry,I couldn't find information about {query} on wikipedia.")
                

        elif "calculate" in query:
            calculation_query = query.lower().split("calculate", 1)[1].strip()
            model_response = wolfram_alpha_query(calculation_query)
            
        elif "open youtube" in query:
            webbrowser.open("youtube.com")
            model_response = "Opening youtube..."

        elif "open google" in query:
            webbrowser.open("google.com")
            model_response = "Opening google..."

        elif "open powerful gpt" in query or "chatgpt" in query or "chat GPT" in query:
            webbrowser.open("https://chat.openai.com/")
            model_response = "Opening ChatGPT..."

        elif "current time" in query:
            webbrowser.open("https://www.timeanddate.com/worldclock/india/new-delhi")
            model_response = "Opening current time..."

        elif "open stack overflow" in query:
            webbrowser.open("stackoverflow.com")
            model_response = "Opening stack overflow..."

        elif "open leet code" in query or "open lead code" in query:
            webbrowser.open("leetcode.com")
            model_response = "Opening leet code..."
        elif "open suraj facebook" in query:
            webbrowser.open("https://www.facebook.com/")
            model_response = "Opening facebook..."
        elif "play music" in query:
            a = random.randint(0, 15)
            music_dir = "C:\\Users\\SURAJ PANDEY\\Music\\music"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[a]))
            model_response = "Playing music..."

        elif "play video" in query:
            b = random.randint(0, 10)
            video_dir = "C:\\Users\\SURAJ PANDEY\\Videos\\video"
            videos = os.listdir(video_dir)
            print(videos)
            os.startfile(os.path.join(video_dir, videos[b]))
            model_response = "Playing video..."

        elif "the time" in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            #speak(f"Sir, the time is {strTime}")
            model_response = f"Sir, the time is {strTime}"
        elif "the date" in query:
            strftime = datetime.now().strftime("%d/%m/%Y")
            #speak(f"Sir, the date is {strftime}")
            model_response = f"Sir, the date is {strftime}"

        elif "open code" in query:
            codePath = "C:\\Users\\SURAJ PANDEY\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            model_response = "Opening Visual Studio Code..."

        elif "wikipedia about" in query:
            query = query.replace("tell me about", "")
            if check_page_exists(query):
                summary = get_summary(query)
                print(summary)
                model_response = summary
                #speak(summary)

                page_url = get_page_url(query)
                print("Wikipedia URL:", page_url)
                model_response = f"{summary}\nWikipedia URL: {page_url}"
                webbrowser.open(page_url)

            else:
                general_response = "I' m sorry, but i could't find just now makebe its not valid page title,please provide valid page title..."
                #speak(general_response)
                model_response = general_response


        elif "rajkiya engineering college azamgarh" in query:
            #speak(
            #    "Rajkiya Engineering College, Azamgarh (formerly MKECIT) was established in 2007 and began offering B.Tech. programs in Information Technology, Mechanical Engineering, and Civil Engineering from 2010. Its aim is to provide education, conduct research, and lead in technological innovation for industrial and infrastructural development."
            #)
            print(
                "Rajkiya Engineering College, Azamgarh (formerly MKECIT) was established in 2007 and began offering B.Tech. programs in Information Technology, Mechanical Engineering, and Civil Engineering from 2010. Its aim is to provide education, conduct research, and lead in technological innovation for industrial and infrastructural development."
            )
            webbrowser.open("https://www.gecazamgarh.ac.in/")
            model_response = "Rajkiya Engineering College, Azamgarh ."

        elif "open my website" in query or "open suraj website" in query:
            webbrowser.open(
                "https://surajinformationtechnologyportfolio.000webhostapp.com/"
            )
            model_response = "Opening your website..."

            
        elif "thank you" in query or "thank" in query:
            #speak("very very welcome")
            print("very very welcome")
            s = random.randint(0, 2)
            video_dir1 = "C:\\Users\\SURAJ PANDEY\\Downloads\\thanku"
            videos1 = os.listdir(video_dir1)
            print(videos1)
            os.startfile(os.path.join(video_dir1, videos1[s]))
            model_response = "very very welcome"
        #elif "exit" in query:
            model_response = "Goodbye! Have a nice day."
            #speak("Goodbye! Have a nice day.")
            #wishMe1()
            #break

        else:
          #speak(model_response)
          print(model_response)
          chat.history.append({"role": "user", "parts": [query]})
          chat.history.append({"role": "model", "parts": [user_res.text]})
        return model_response