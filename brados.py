# brados.py
import json
import os
import time
from brados_system import clear_screen, display_header, get_menu_choice
from brados_apps import (
    simple_calculator, brad_mail, brad_game_center, brad_hub, 
    task_manager, brad_file_browser, brad_text_editor, brad_browser
) # Import all apps

# --- User Profile Management ---
USER_PROFILE_DIR = "user_profiles"
if not os.path.exists(USER_PROFILE_DIR):
    os.makedirs(USER_PROFILE_DIR)

def get_profile_path(username):
    """Returns the path to a user's profile JSON file."""
    return os.path.join(USER_PROFILE_DIR, f"{username}.json")

def load_user_profile(username):
    """Loads a user's profile, or creates a new one if it doesn't exist."""
    profile_path = get_profile_path(username)
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            profile = json.load(f)
            # Ensure essential keys exist, for backward compatibility
            profile.setdefault('installed_apps', [])
            profile.setdefault('tasks', [])
            profile.setdefault('bradmail_inbox', [])
            profile.setdefault('bradmail_sent', [])
            profile.setdefault('device_type', 'Compute') # Default to Compute if not set
            return profile
    else:
        # Create a new profile with defaults
        new_profile = {
            "username": username,
            "installed_apps": [],
            "tasks": [],
            "bradmail_inbox": [],
            "bradmail_sent": [],
            "device_type": 'Compute' # Default device type for new users
        }
        save_user_profile(new_profile) # Save the new profile immediately
        return new_profile

def save_user_profile(user_profile):
    """Saves the current user profile to its JSON file."""
    profile_path = get_profile_path(user_profile['username'])
    with open(profile_path, 'w') as f:
        json.dump(user_profile, f, indent=4)

# --- BradOS Main System ---
def run_brados():
    clear_screen()
    display_header("Welcome to BradOS! 🚀")

    # --- User Login/Selection ---
    username = input("Enter your username (or type 'new' to create): ").strip()
    if username.lower() == 'new':
        while True:
            new_username = input("Enter a new username: ").strip()
            if not new_username:
                print("Username cannot be empty. 🚫")
                continue
            if os.path.exists(get_profile_path(new_username)):
                print("Username already exists. Please choose another. ⚠️")
            else:
                username = new_username
                break
    
    user_profile = load_user_profile(username)
    print(f"Welcome back, {user_profile['username']}! 👋")
    time.sleep(1)

    # --- Device Type Selection (NEW) ---
    clear_screen()
    display_header("Select Your BradOS Device Type")
    print("Which Brad Device are you using today?")
    print("1. BradOS Mobile 📱 (Optimized for small screens)")
    print("2. BradOS Slate  tablet (Optimized for tablets/medium screens)") # Removed Hindi character
    print("3. BradOS Compute 🖥️ (Optimized for desktops/large screens)")
    
    valid_device_choices = ['1', '2', '3']
    device_choice = get_menu_choice("Enter your choice: ", valid_device_choices)

    device_types = {
        '1': 'Mobile',
        '2': 'Slate',
        '3': 'Compute'
    }
    user_profile['device_type'] = device_types[device_choice]
    save_user_profile(user_profile)
    print(f"BradOS is now running in {user_profile['device_type']} mode. 🎉")
    time.sleep(2)


    # --- Main BradOS Loop ---
    while True:
        clear_screen()
        
        # Enhanced header based on device type
        device_emoji = {
            'Mobile': '📱',
            'Slate': '💻', # Using a laptop emoji for slate, could also be ' टैबलेट' but let's stick to English characters
            'Compute': '🖥️'
        }
        current_device_emoji = device_emoji.get(user_profile['device_type'], '❓')
        display_header(f"BradOS {user_profile['device_type']} {current_device_emoji} - Main Menu 🏠")
        
        print(f"Logged in as: {user_profile['username']} | Device: {user_profile['device_type']}")
        print("\n--- Applications ---")
        
        # Define applications based on device type
        available_apps = {}
        if user_profile['device_type'] == 'Mobile':
            available_apps = {
                '1': {'name': 'BradMail 📧', 'func': brad_mail},
                '2': {'name': 'BradGame Center 🕹️', 'func': brad_game_center},
                '3': {'name': 'Task Manager ✅📋', 'func': task_manager},
                '4': {'name': 'BradBrowser 🌐', 'func': brad_browser},
            }
        elif user_profile['device_type'] == 'Slate':
            available_apps = {
                '1': {'name': 'Simple Calculator ➕➖', 'func': simple_calculator},
                '2': {'name': 'BradMail 📧', 'func': brad_mail},
                '3': {'name': 'BradGame Center 🕹️', 'func': brad_game_center},
                '4': {'name': 'Task Manager ✅📋', 'func': task_manager},
                '5': {'name': 'BradHub 🌐🛍️', 'func': brad_hub},
                '6': {'name': 'BradFileBrowser 📁', 'func': brad_file_browser},
                '7': {'name': 'BradBrowser 🌐', 'func': brad_browser},
            }
        else: # Default to 'Compute'
            available_apps = {
                '1': {'name': 'Simple Calculator ➕➖', 'func': simple_calculator},
                '2': {'name': 'BradMail 📧', 'func': brad_mail},
                '3': {'name': 'BradGame Center 🕹️', 'func': brad_game_center},
                '4': {'name': 'BradHub 🌐🛍️', 'func': brad_hub},
                '5': {'name': 'Task Manager ✅📋', 'func': task_manager},
                '6': {'name': 'BradFileBrowser 📁', 'func': brad_file_browser},
                '7': {'name': 'BradTextEditor 📝', 'func': brad_text_editor},
                '8': {'name': 'BradBrowser 🌐', 'func': brad_browser},
            }

        # Display available apps
        for key, app_data in available_apps.items():
            print(f"{key}. {app_data['name']}")
        
        # Add system options
        menu_options = {
            **available_apps, # Merge app options
            's': {'name': 'System Settings ⚙️'}, # Placeholder for future
            'c': {'name': 'Clear Screen 🧹'},
            'l': {'name': 'Logout 🚪'},
            'x': {'name': 'Shutdown BradOS 🛑'}
        }

        print("\n--- System Options ---")
        print("s. System Settings ⚙️")
        print("c. Clear Screen 🧹")
        print("l. Logout 🚪")
        print("x. Shutdown BradOS 🛑")
        print("----------------------")

        valid_choices = list(menu_options.keys())
        choice = get_menu_choice("Enter your choice: ", valid_choices)

        if choice in available_apps:
            app_func = available_apps[choice]['func']
            if app_func in [brad_mail, brad_hub, task_manager]: # Apps that need profile access
                app_func(user_profile, save_user_profile)
            else: # Apps that don't currently need profile access
                app_func() 
            time.sleep(1) # Give a moment after app exits
        elif choice == 's':
            display_header("System Settings ⚙️")
            print("System settings not yet implemented. Stay tuned! 🛠️")
            input("\nPress Enter to continue... ↩️")
        elif choice == 'c':
            clear_screen()
        elif choice == 'l':
            print("Logging out... Goodbye! 👋")
            time.sleep(2)
            run_brados() # Restart BradOS for new login
            return # Exit current instance
        elif choice == 'x':
            print("Shutting down BradOS... See you next time! 💤")
            time.sleep(3)
            clear_screen()
            break # Exit the main loop

# Entry point
if __name__ == "__main__":
    run_brados()
                
