import customtkinter as ctk
import tkinter as tk
from PIL import Image  # Import the Image class from Pillow

# Create the main application window
app = ctk.CTk()
app.title("Hover to Reveal")

# Get screen dimensions
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculate vertical center of the screen
vertical_center = (screen_height // 2) - 15  # Subtract half the height of the app (15px for 30px total height)

# Set the initial position to the left side, vertically centered
app.geometry(f"200x30+0+{vertical_center}")

# Remove the title bar and window decorations
app.overrideredirect(True)

# Set the window to always be on top
app.wm_attributes('-topmost', 1)

# Load the image using Pillow
arrow_image_path = "images/arrows-of-four-direction.jpg"
arrow_pil_image = Image.open(arrow_image_path)  # Open the image file
arrow_image = ctk.CTkImage(light_image=arrow_pil_image, size=(30, 30))  # Convert to CTkImage

# Variable to track if the button is being held
button_pressed = False

# Function to handle moving the window
def start_move(event):
    if not button_pressed:  # Only allow move if the button is not pressed
        app.x = event.x
        app.y = event.y

def move_window(event):
    if not button_pressed:  # Only allow move if the button is not pressed
        app.geometry(f"+{app.winfo_x() + event.x - app.x}+{app.winfo_y() + event.y - app.y}")

# Function to set opacity to 100% on hover
def on_enter(event):
    app.wm_attributes('-alpha', 1.0)

# Function to reduce opacity when not hovering
def on_leave(event):
    app.wm_attributes('-alpha', 1.0)  # Keep at 100% initially
    app.after(1000, lambda: app.wm_attributes('-alpha', 0.2))  # Reduce to 20% after 1 second

# Function to snap the window to the edge of the screen and adjust layout
def snap_to_edge():
    window_x = app.winfo_x()

    if window_x < screen_width / 2:  # If the window is in the left half
        app.geometry(f"+0+{app.winfo_y()}")  # Snap to the left edge
        left_image_label.pack(side=tk.RIGHT)  # Show the left image
        right_image_label.pack_forget()  # Hide the right image
        main_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Attach main button to the left edge
    else:  # If the window is in the right half
        app.geometry(f"+{screen_width - app.winfo_width()}+{app.winfo_y()}")  # Snap to the right edge
        right_image_label.pack(side=tk.LEFT)  # Show the right image
        left_image_label.pack_forget()  # Hide the left image
        main_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Attach main button to the right edge

# Create a frame to hold the components
frame = ctk.CTkFrame(app)
frame.pack(fill=tk.BOTH, expand=True)

# Create left image label (just an image, no button)
left_image_label = ctk.CTkLabel(frame, image=arrow_image, text="")

# Create main button
main_button = ctk.CTkButton(frame, text="Main", command=lambda: print("Main button clicked!"))

# Create right image label (just an image, no button)
right_image_label = ctk.CTkLabel(frame, image=arrow_image, text="")

# Set button press state on button press/release
def on_button_press(event):
    global button_pressed
    button_pressed = True

def on_button_release(event):
    global button_pressed
    button_pressed = False

# Initial layout
left_image_label.pack_forget()  # Hide left image initially
main_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
right_image_label.pack(side=tk.LEFT)

# Adjust the window height to match the button height
def adjust_window_height():
    app.geometry(f"{app.winfo_width()}x{main_button.winfo_height()}")

app.after(10, adjust_window_height)

# Set initial opacity to 100% for 10 seconds, then reduce to 20%
app.wm_attributes('-alpha', 1.0)
app.after(10000, lambda: app.wm_attributes('-alpha', 0.2))  # After 10 seconds, set opacity to 20%

# Bind hover events for the frame
frame.bind("<Enter>", on_enter)
frame.bind("<Leave>", on_leave)

# Bind window dragging
app.bind("<Button-1>", start_move)
app.bind("<B1-Motion>", move_window)

# Bind the window to snap to the edge when it is released
app.bind("<ButtonRelease-1>", lambda event: snap_to_edge())

# Bind button press and release to toggle the drag behavior
main_button.bind("<ButtonPress-1>", on_button_press)
main_button.bind("<ButtonRelease-1>", on_button_release)

# Start the application
app.mainloop()
