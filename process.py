from collections import Counter
import emoji

def analyze_data(messages_df):
    most_common_words = Counter(" ".join(messages_df['content']).split()).most_common(10)
    most_common_emojis = Counter("".join([emoji for sublist in messages_df['emojis'] for emoji in sublist])).most_common(10)
    most_active_senders = messages_df['sender'].value_counts().head(10)
    
    return most_common_words, most_common_emojis, most_active_senders

most_common_words, most_common_emojis, most_active_senders = analyze_data(messages_df)
print("Most common words:", most_common_words)
print("Most common emojis:", most_common_emojis)
print("Most active senders:", most_active_senders)
