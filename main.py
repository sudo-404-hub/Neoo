# main.py
import threading
import customtkinter as ctk
import speech_recognition as sr 
import pyttsx3
from which_type_query import which_type_query_fun
# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Configure the appearance of the customtkinter app
ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("green")  # Choose your color theme (or use "blue" or "dark-blue")

# Create the main application
app = ctk.CTk()  # Initialize the customtkinter window
app.title("Matrix AI")
app.geometry("800x500")  # Set the window size

# Add a frame to hold the terminal output and input
frame = ctk.CTkFrame(app)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Add a scrollable text area for the terminal output
terminal_output = ctk.CTkTextbox(
    frame,
    height=400,
    width=750,
    wrap="word",
    state="disabled",  # Initially disabled (to prevent direct editing)
    font=("Courier", 12),  # Use a monospace font like Linux terminals
)
terminal_output.pack(fill="both", expand=True, padx=5, pady=5)

# Frame for the command input and buttons
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=10, pady=5)

# Left button (Voice Off / Mic On)
voice_button = ctk.CTkButton(input_frame, text="Voice Off", width=10, command=lambda: toggle_voice())
voice_button.pack(side="left", padx=(0, 10))

# Input field for commands
command_input = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type here...",
    font=("Courier", 12),
)
command_input.pack(side="left", fill="x", expand=True, padx=10)

# Right button (Send Command)
send_button = ctk.CTkButton(input_frame, text="Send", width=10, command=lambda: run_command())
send_button.pack(side="right", padx=(10, 0))

# State for voice (microphone on/off)
voice_state = False  # Initially 'Voice Off'


# Function to toggle voice state
def toggle_voice():
    # convert min of to on
    global voice_state
    voice_button.configure(text="Mic On")
    app.update()
    voice_state = True
        
    # function to take voice input
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Listening...")
        try:
            audio = recognizer.listen(source)
            input_text = recognizer.recognize_google(audio)# main output of voice 
            # print(input_text) 

            voice_command(input_text)
            voice_button.configure(text="Voice Off")
            app.update()
            voice_state = False
            

        except sr.UnknownValueError:
            print("Could not understand the audio.")
            voice_button.configure(text="Voice Off")
            app.update()
            voice_state = False
            
        except sr.RequestError:
            print("Speech recognition service error.")
            voice_button.configure(text="Voice Off")
            app.update()
            voice_state = False
            
    # engine.runAndWait()


# print the message in UI 
def print_on_ui_terminal(message):
    # Append the query and the output to the terminal
    terminal_output.configure(state="normal")  # Enable editing
    terminal_output.insert("end", f"{message}\n")  # Show the query and output from the function
    terminal_output.configure(state="disabled")  # Disable editing
    terminal_output.see("end")  # Scroll to the bottom of the terminal
    command_input.delete(0, "end")  # Clear the input field


def voice_command(voice_text):
    try:
        print_on_ui_terminal(voice_text)  # Print the command on UI
        app.update()  # Update the UI to render voice command
        ai_output = which_type_query_fun(voice_text)  # Call AI to give response
        print_on_ui_terminal(ai_output)  # Print output on UI
        app.update()  # Update the UI to render output
        engine.say(ai_output)  # Speak the AI output
        engine.runAndWait()  # Wait until speaking AI response
    except Exception as e:
        print_on_ui_terminal(f"Error: {str(e)}")  # Print error message on UI

def run_command():
    command = command_input.get()
    if command.strip():  # Make sure the command is not empty
        try:
            print_on_ui_terminal(command)  # Print the command on UI
            app.update() 
            ai_output = which_type_query_fun(command)  # Call AI to give response
            print_on_ui_terminal(ai_output)  # Print output on UI
            app.update()
            engine.say(ai_output)  # Speak the AI output
            engine.runAndWait()  # Wait until speaking AI response
        except Exception as e:
            print_on_ui_terminal(f"Error: {str(e)}")  # Print error message on UI





# Bind the Enter key to the run_command function
command_input.bind("<Return>", lambda event: run_command())


# Run the application
app.mainloop()
