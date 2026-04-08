import requests

def fetch_github_stats(username):
    """
    Fetches real GitHub stats and commit analytics for a given username.
    """
    base_url = f"https://api.github.com/users/{username}"
    events_url = f"https://api.github.com/users/{username}/events/public"
    repos_url = f"{base_url}/repos?per_page=100"
    search_commits_url = f"https://api.github.com/search/commits?q=author:{username}"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Stats-Analyzer"
    }

    try:
        # Fetch user info
        user_response = requests.get(base_url, headers=headers)
        if user_response.status_code != 200:
            print(f"Error: User '{username}' not found.")
            return

        user_data = user_response.json()
        
        # Fetch repos info
        repos_response = requests.get(repos_url, headers=headers)
        repos_data = repos_response.json() if repos_response.status_code == 200 else []

        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        languages = {}
        for repo in repos_data:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

        # Fetch total commits (Search API)
        commit_search_response = requests.get(search_commits_url, headers={"Accept": "application/vnd.github.cloak-preview"})
        total_commits = commit_search_response.json().get('total_count', 0) if commit_search_response.status_code == 200 else 0

        # Fetch REAL-TIME latest activity (Events API)
        # This is much faster and more accurate than Search API for "Latest"
        events_response = requests.get(events_url, headers=headers)
        latest_activity_str = "N/A"
        daily_activity = {}

        if events_response.status_code == 200:
            events = events_response.json()
            if events:
                # The first event is the latest one
                raw_date = events[0].get('created_at')
                if raw_date:
                    try:
                        from datetime import datetime
                        dt = datetime.strptime(raw_date[:19], "%Y-%m-%dT%H:%M:%S")
                        latest_activity_str = dt.strftime("%b %d, %Y %H:%M")
                    except:
                        latest_activity_str = raw_date

                # Aggregate activity for simple peak analysis from recent events
                for event in events:
                    date_str = event.get('created_at', '')[:10]
                    if date_str:
                        daily_activity[date_str] = daily_activity.get(date_str, 0) + 1

        print(f"\n--- GitHub Stats for {username} ---")
        print(f"Name: {user_data.get('name', 'N/A')}")
        print(f"Bio: {user_data.get('bio', 'N/A')}")
        print(f"Public Repos: {user_data.get('public_repos', 0)}")
        print(f"Followers: {user_data.get('followers', 0)}")
        print(f"Total Stars: {total_stars}")
        print(f"Total Commits: {total_commits}")
        print(f"Real-time Latest Activity: {latest_activity_str}")
        
        if daily_activity:
            highest_day = max(daily_activity, key=daily_activity.get)
            lowest_day = min(daily_activity, key=daily_activity.get)
            print(f"Highest Activity: {daily_activity[highest_day]} commits ({highest_day})")
            print(f"Lowest Activity: {daily_activity[lowest_day]} commits ({lowest_day})")
        
        if languages:
            top_lang = max(languages, key=languages.get)
            print(f"Primary Language: {top_lang}")
            
        print("\nTop Repositories:")
        sorted_repos = sorted(repos_data, key=lambda x: x.get('stargazers_count', 0), reverse=True)[:5]
        for repo in sorted_repos:
            print(f"- {repo['name']} (⭐ {repo['stargazers_count']})")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("GitHub Stats Analyzer")
    username = input("Enter GitHub username: ").strip()
    if username:
        fetch_github_stats(username)
    else:
        print("Username cannot be empty.")

if __name__ == "__main__":
    main()
