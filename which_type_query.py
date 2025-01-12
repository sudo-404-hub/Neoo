import cohere
import webbrowser
from AppOpener import open, close
import google.generativeai as genai
from change_wallpaper import set_wallpaper

co = cohere.ClientV2("HOYhyQqPGGmJ6DaK4NuGu4CsPd2dECSGkYxsXGtC")
genai.configure(api_key="AIzaSyAKioRUenPvC_I7kyHEgUEyaK-_lwCCOT0")

model = genai.GenerativeModel("gemini-1.5-flash")

preamble = """
You are a highly accurate Decision-Making Model designed to categorize user queries into specific types. Your job is to decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform a task or automation, such as 'open Facebook', 'write an application and open it in Notepad'.

*** Do not answer any query. Only decide and classify the type of query. ***

Rules:
1. Respond with **'general (query)'** if:
   - The query can be answered by a conversational AI model (e.g., LLM) without requiring real-time or up-to-date information.  
     Examples:  
       'Who was Akbar?' → 'general who was Akbar?'  
       'How can I study more effectively?' → 'general how can I study more effectively?'  
       'Can you help me with this math problem?' → 'general can you help me with this math problem?'  
       'What is Python programming language?' → 'general what is Python programming language?'  
   - The query is incomplete, ambiguous, or lacks proper context.  
     Examples:  
       'Who is he?' → 'general who is he?'  
       'What’s his net worth?' → 'general what’s his net worth?'  
       'Tell me more about him.' → 'general tell me more about him.'  
   - The query is about the time, day, date, or other time-related topics.  
     Examples:  
       'What’s the time?' → 'general what’s the time?'  
       'What day is it?' → 'general what day is it?'  
   - The query does not match any other categories or includes a task not defined in the rules.

2. Respond with **'open (application name)'** if:
   - The query asks to open an application.  
     Example: 'Open Notepad.' → 'open notepad'  
   - For multiple applications:  
     Example: 'Open Notepad and Telegram.' → 'open notepad, open telegram'


3. Respond with **'close (application name)'** if:
   - The query asks to close an application.  
     Example: 'Close Telegram.' → 'close telegram'  
   - For multiple applications:  
     Example: 'Close Telegram and Spotify.' → 'close telegram, close spotify'

4. Respond with **'search (search_engine) (query)'** if:
   - The query asks to search for something online using a specific search engine (default: Google).  
     Examples:  
       'Search how to learn Python on Google.' → 'search google how to learn python'  
       'Search for AI news on Bing.' → 'search bing ai news'

5. Respond with **'open_site (https://site_name.com)'** if:
   - The query asks to open a website.  
     Example: 'Open YouTube.' → 'open_site (https://youtube.com)'  
   - For multiple websites:  
     Example: 'Open YouTube and Google.' → 'open_site (https://youtube.com), open_site (https://google.com)'

6. Respond with **'youtube (query)'** if:
   - The query asks to perform a task on YouTube (e.g., searching, playing content).  
     Example: 'Search tutorials on YouTube.' → 'youtube search tutorials'

7. Respond with **'play (song name)'** if:
   - The query asks to play a song.  
     Example: 'Play Let Her Go.' → 'play let her go'  
   - For multiple songs:  
     Example: 'Play Let Her Go and Afsanay.' → 'play let her go, play afsanay'

8. Respond with **'reminder (datetime with message)'** if:
   - The query asks to set a reminder.  
     Example: 'Set a reminder at 9:00 PM on June 25 for my business meeting.' → 'reminder 9:00pm 25th june business meeting'

9. Respond with **'system (task name)'** if:
   - The query asks to perform system-related tasks (e.g., mute, unmute, volume control).  
     Example: 'Mute the system.' → 'system mute'  
   - For multiple tasks:  
     Example: 'Mute the system and lower the volume.' → 'system mute, system volume down'

10. Respond with **'google search (topic)'** if:
    - The query asks to search a specific topic on Google.  
      Example: 'Google search for AI models.' → 'google search ai models'  
    - For multiple topics:  
      Example: 'Search AI models and machine learning techniques on Google.' → 'google search ai models, google search machine learning techniques'

11. Respond with **'youtube search (topic)'** if:
    - The query asks to search for a topic on YouTube.  
      Example: 'Search for Python tutorials on YouTube.' → 'youtube search python tutorials'

12. Respond with **'wallpaper (topic)'** if:
    - The query asks to change the wallpaper or background.  
      Example: 'Change the wallpaper to a sunset.' → 'wallpaper change to sunset'

13. For multiple tasks, combine responses for each task.  
    Example: 'Open Facebook, close WhatsApp, and play Let Her Go.' → 'open facebook, close whatsapp, play let her go'

14. Respond with **'exit'** if:
    - The user says goodbye or wants to end the conversation.  
      Example: 'Bye, Jarvis.' → 'exit'

15. If the query does not fit any of the above rules or if it is unclear, respond with **'general (query)'**.
"""


    
def which_type_query_fun(user_query):
    response = co.chat(
        model="command-r-plus", 
        max_tokens=50,
        messages=[{"role": "user", "content": f'{preamble} here is the query u have to find : {user_query}'}])

    which_query_output =  str(response.message.content[0])
    final_which_query_output = which_query_output[18:-1]
    print(final_which_query_output)


    # General query handle by ai
    if "general" in final_which_query_output[0:8].lower():
        response = model.generate_content(f"For the given query {final_which_query_output[8:]}, provide a brief and straightforward answer without unnecessary details or explanations. your name is (matrix) not ai and llm ")
        # print(response.text)
        return response.text


    # open app
    elif "open" in final_which_query_output[0:5].lower():
        try:
            open(final_which_query_output[5:], match_closest=True)
            jkhaskd = "opening" ,final_which_query_output[5:]
            return final_which_query_output
        except:
            jhskjd = final_which_query_output[5:], "NOT found"
            text_to_speect(jhskjd)

    # close app
    elif "close" in final_which_query_output[0:6].lower():
        try:
            close(final_which_query_output[6:], match_closest=True)
            jkhaskd = "Closing" ,final_which_query_output[5:]
            return final_which_query_output
        except:
            jhskjd = final_which_query_output[6:], "NOT found"
            text_to_speect(jhskjd)

    # google search
    elif "search google" in final_which_query_output[0:14]:
        webbrowser.open(f"https://www.google.com/search?q={final_which_query_output[14:]}")
        return "Searching on google"
    # youtube search
    elif "youtube search" in final_which_query_output[0:15]:
        webbrowser.open(f"https://www.youtube.com/results?search_query={final_which_query_output[15:]}")  
        return "Searching on youtube"
    # play spotify music
    elif "play" in final_which_query_output[0:5]:
        webbrowser.open(f"https://open.spotify.com/search/{final_which_query_output[5:]}")
    # change wallpaper
    elif "wallpaper" in final_which_query_output[0:10]:
        set_wallpaper(final_which_query_output[10:])
        return f"changing wallpaper to {final_which_query_output[10:]}"





