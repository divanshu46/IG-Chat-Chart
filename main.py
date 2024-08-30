import json
import pandas as pd
import emoji
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import matplotlib.font_manager as fm


# Set up the fonts
default_font = 'DejaVu Sans'
backup_font_path = r'C:\Users\MP-MOH-LAP-D121\AppData\Local\Microsoft\Windows\Fonts\NotoSansDevanagari-VariableFont_wdth,wght.ttf'
fm.fontManager.addfont(backup_font_path)
backup_font_prop = fm.FontProperties(fname=backup_font_path)
backup_font_name = backup_font_prop.get_name()
plt.rcParams['font.family'] = [backup_font_name, 'sans-serif']

# Load multiple JSON files
def load_json(file_paths):
    all_data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            all_data.extend(data['messages'])  # Add all messages from each file
    return all_data

def decode_n(encoded_string):
    return encoded_string.encode('latin1').decode('utf-8')

# Extract emojis from text
def extract_emojis(text):
    return [char for char in text if emoji.is_emoji(char)]

def identify_attachment_message(message):
    # Regular expression pattern to match "<name> sent an attachment."
    pattern = r"([^\s]+) sent an attachment\."
    match = re.search(pattern, message)
    
    if match:
        return True
    else:
        return False

# Extract messages from JSON data
def extract_messages(data):
    messages = []
    
    for message in data:
        ignore_phrase1 = "आपके मैसेज"
        ignore_phrase2 = "मैसेज को लाइक किया है"
        sender = decode_n(message.get('sender_name', 'Unknown'))
        timestamp = message.get('timestamp_ms', 0)
        content = decode_n(message.get('content', ''))
        if ignore_phrase1 in content:
            emojis = extract_emojis(content)
            content = ''  # Ignore the rest of the content
        else:
            emojis = extract_emojis(content)
        if ignore_phrase2 in content:
            content = ''  # Ignore the rest of the content
        if identify_attachment_message(content):
            content = " "
        reactions = []
        if 'reactions' in message:
            reactions = [extract_emojis(reaction['reaction']) for reaction in message['reactions']]
        
        # Flatten the list of reactions
        flattened_reactions = [emoji for sublist in reactions for emoji in sublist]
        
        messages.append({
            'sender': sender,
            'timestamp': timestamp,
            'content': content,
            'emojis': emojis,
            'reactions': flattened_reactions
        })
    
    return pd.DataFrame(messages)

plt.style.use(r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\styles\rose-pine.mplstyle")

# Analyze the data
def analyze_data(messages_df):
    most_common_words = Counter(" ".join(messages_df['content']).split()).most_common(20)
    most_common_emojis = Counter("".join([emoji for sublist in messages_df['emojis'] for emoji in sublist])).most_common(10)
    most_active_senders = messages_df['sender'].value_counts().head(10)
    phrase_counts = messages_df[messages_df['content'].str.contains(specific_phrase, case=False, na=False)]['sender'].value_counts()
    
    return most_common_words, most_common_emojis, most_active_senders, phrase_counts

# Plot the analyzed data
def plot_data(most_common_words, most_common_emojis, most_active_senders, specific_phrase, phrase_counts):
    # Plot most common words
    words, counts = zip(*most_common_words)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(counts), y=list(words))
    plt.title('Most Common Words')
    plt.show()

    # Plot most common emojis
    emojis, counts = zip(*most_common_emojis)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(counts), y=list(emojis))
    plt.title('Most Common Emojis')
    plt.show()

    # Plot most active senders
    plt.figure(figsize=(10, 5))
    sns.barplot(x=most_active_senders.values, y=most_active_senders.index)
    plt.title('Most Active Senders')
    plt.show()

    # Plot occurrences of specific phrase
    plt.figure(figsize=(10, 5))
    sns.barplot(x=phrase_counts.values, y=phrase_counts.index)
    plt.title(f'Occurrences of "{specific_phrase}" by Sender')
    plt.xlabel('Occurrences')
    plt.ylabel('Sender')
    plt.show()

# Example usage with multiple JSON files
file_paths = [r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_1_rb.json"]
              
            #   r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_2.json",
            #   r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_3.json",
            #   r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_4.json",
            #   r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_5.json",
            #   r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_6.json",
            #   r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_7.json",
            #   r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_8.json"

data = load_json(file_paths)
messages_df = extract_messages(data)
messages_df.to_csv('data.csv', index=False)
specific_phrase = "bubu"

# Process and analyze the DataFrame
most_common_words, most_common_emojis, most_active_senders, phrase_counts = analyze_data(messages_df)

# Plot the results
plot_data(most_common_words, most_common_emojis, most_active_senders, specific_phrase, phrase_counts)
