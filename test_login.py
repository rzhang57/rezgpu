from services.ig_client import get_ig_client

ig = get_ig_client()

user = ig.user_info_by_username_v1("suswindow")
print(f"Fetched user: {user.username}, followers: {user.follower_count}")