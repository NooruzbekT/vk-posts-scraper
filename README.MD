# VK Group Posts Scraper 

This script collects posts from VK groups using the VK API, processes them, and saves the extracted data in a CSV file. It includes logging, request handling, and content classification.

## Features  
- Fetches posts from multiple VK groups.  
- Extracts key data such as text, likes, comments, reposts, hashtags, and content type.  
- Handles request limits and API errors with logging.  
- Saves structured data in a CSV file for further analysis.

## Requirements 
- Python 3.10.15
- requests 2.31.0 
- IDE: PyCharm or VS Code (code written in PyCharm)

## Installation  

1. **Clone the repository:**  
   ```sh
   git clone https://github.com/NooruzbekT/vk-posts-scraper  
    ```
2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required dependencies:
    ```sh
    pip install requests==2.31.0
    ```
   
## VK API Configuration

### 1. Obtain an access token:
- Go to VK Developer and create an application.
- Generate an API token with wall access permissions.
### 2. Set up your token in the script:
- Replace access_token in `vk_scraper.py` with your actual token.

## Usage

Run the script to start collecting posts:
```sh
   python vk_scraper.py
```

## Output

- The script saves the extracted data in a CSV file named "filtered_vk_posts9.csv" in the same directory.

## Logging

- Logs are saved in `vk_scraper.log`.
- The script uses a rotating log system to manage file size.

## Notes

- Ensure your VK API token has the correct permissions.
- The script automatically handles API request limits with pauses.
- Modify the group_ids list to specify which groups to scrape.

## Data Structure

The collected posts are saved in a CSV file (`filtered_vk_posts9.csv`) with the following columns:

| Column Name   | Description |
|--------------|------------|
| **Post ID**  | Unique identifier of the post |
| **Post Link** | Direct link to the post on VK |
| **Text**  | Content of the post (truncated to 500 characters) |
| **Date & Time**  | UTC timestamp of when the post was published |
| **Author ID**  | ID of the group or user who posted it |
| **Likes**  | Number of likes on the post |
| **Comments**  | Number of comments under the post |
| **Reposts**  | Number of times the post was shared |
| **Hashtags**  | Extracted hashtags from the post text |
| **Content Type**  | Categorization based on attachments and text presence |
| **Text Length**  | Length of the post text |
| **Time of Day**  | Classification of when the post was made (Morning, Day, Evening, Night) |

The extracted data is stored in CSV format, allowing easy analysis and further processing.

## Contact

For any inquiries or issues, please contact `nookentoktobaev@gmail.com`.


