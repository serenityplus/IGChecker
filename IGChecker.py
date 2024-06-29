import os
from getpass import getpass
from instaloader import Instaloader, Profile, LoginRequiredException, BadCredentialsException

print("=" * 50)
print("IGChecker".center(50))
print("By @serenityservice".center(50))
print("https://github.com/anonymous777bob/IGChecker".center(50))
print("=" * 50)

def fetch_instagram_data(loader, username):
    try:
        # Load profile
        profile = Profile.from_username(loader.context, username)
        
        # Get followers and followings
        followers = [follower.username for follower in profile.get_followers()]
        followings = [following.username for following in profile.get_followees()]
        
        return followers, followings
    except LoginRequiredException:
        print("Login required to access followers and followings. Please check your credentials.")
        return [], []

def save_data_to_txt(username, followers, followings):
    folder_name = f"{username}_followers"
    os.makedirs(folder_name, exist_ok=True)
    
    with open(os.path.join(folder_name, 'followers.txt'), 'w') as f:
        for follower in followers:
            f.write(f"{follower}\n")
    
    with open(os.path.join(folder_name, 'followings.txt'), 'w') as f:
        for following in followings:
            f.write(f"{following}\n")

def load_data_from_txt(username):
    folder_name = f"{username}_followers"
    
    followers_path = os.path.join(folder_name, 'followers.txt')
    followings_path = os.path.join(folder_name, 'followings.txt')
    
    if not os.path.exists(followers_path) or not os.path.exists(followings_path):
        return None, None
    
    with open(followers_path, 'r') as f:
        followers = [line.strip() for line in f.readlines()]
    
    with open(followings_path, 'r') as f:
        followings = [line.strip() for line in f.readlines()]
    
    return followers, followings

def save_credentials(insta_username, insta_password):
    creds_folder = 'credentials'
    os.makedirs(creds_folder, exist_ok=True)
    
    with open(os.path.join(creds_folder, 'username.txt'), 'w') as f:
        f.write(insta_username)
    
    with open(os.path.join(creds_folder, 'password.txt'), 'w') as f:
        f.write(insta_password)

def load_credentials():
    creds_folder = 'credentials'
    
    try:
        with open(os.path.join(creds_folder, 'username.txt'), 'r') as f:
            insta_username = f.read().strip()
        
        with open(os.path.join(creds_folder, 'password.txt'), 'r') as f:
            insta_password = f.read().strip()
        
        return insta_username, insta_password
    except FileNotFoundError:
        return None, None

def compare_data(old_data, new_data):
    return list(set(old_data) - set(new_data))

def main():
    # Load saved credentials
    insta_username, insta_password = load_credentials()
    
    if insta_username is None or insta_password is None:
        # Prompt for credentials if not saved
        insta_username = input("Enter your Instagram username: ")
        insta_password = getpass("Enter your Instagram password: ")
        
        # Save credentials
        save_credentials(insta_username, insta_password)
        print("Credentials saved successfully!")
    else:
        print("Using saved credentials.")
    
    # Initialize Instaloader
    loader = Instaloader()
    
    try:
        loader.login(insta_username, insta_password)
        print("Logged in successfully!")
    except BadCredentialsException:
        print("Login failed. Check your username and password.")
        return
    
    # Fetch current data
    username_to_track = input("Enter Instagram username to track: ")
    current_followers, current_followings = fetch_instagram_data(loader, username_to_track)
    
    # Load previous data
    old_followers, old_followings = load_data_from_txt(username_to_track)
    
    if old_followers is not None and old_followings is not None:
        # Compare data
        unfollowers = compare_data(old_followers, current_followers)
        unfollowed = compare_data(old_followings, current_followings)
        
        if unfollowers:
            print("Users who unfollowed you:")
            for user in unfollowers:
                print(user)
        
        if unfollowed:
            print("Users you have unfollowed:")
            for user in unfollowed:
                print(user)
    else:
        print("No previous data found. Saving current data.")
    
    # Save current data
    save_data_to_txt(username_to_track, current_followers, current_followings)

if __name__ == "__main__":
    main()
