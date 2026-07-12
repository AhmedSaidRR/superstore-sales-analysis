import os
import urllib.request
import sys

def download_file(urls, dest_path):
    print("Starting download process...")
    # Ensure directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    for url in urls:
        try:
            print(f"Trying to download from: {url}")
            # Add a user-agent to avoid HTTP 403 Forbidden
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Successfully downloaded and saved to {dest_path}")
            return True
        except Exception as e:
            print(f"Failed to download from {url}. Error: {e}")
            
    return False

if __name__ == "__main__":
    urls_to_try = [
        "https://raw.githubusercontent.com/praveen-kumar-maurya/Superstore-Sales-Dashboard-Power-BI/main/Sample%20-%20Superstore.csv",
        "https://raw.githubusercontent.com/eyowhite/Data-Analysis/master/Sample%20-%20Superstore.csv",
        "https://raw.githubusercontent.com/datsoftlyngby/soft2021fall-db/main/Interactive%20Dashboards/Sample%20-%20Superstore.csv",
        "https://raw.githubusercontent.com/tirthajyoti/Machine-Learning-with-Python/master/Datasets/US%20Superstore%20data.csv"
    ]
    
import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(BASE_DIR, 'data', 'raw', 'superstore.csv')
    success = download_file(urls_to_try, dest)
    if not success:
        print("Error: Could not download the Superstore dataset from any of the URLs.")
        sys.exit(1)
    else:
        print("Download completed successfully.")
