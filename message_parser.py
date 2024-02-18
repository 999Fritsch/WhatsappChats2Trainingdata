import re
from datetime import datetime
import tiktoken
import glob

class Message():
    # Regular expression pattern to match date, time, username/number, and message text
    pattern = r"\[(\d{2}[./]\d{2}[./](?:\d{2}| \d{2}))[, ]? ([0-9:.\s]+(?:AM|PM|a\.m\.|p\.m\.|nachm\.|vorm\.|morgens))\] (.+?):\s*(.*(?:\n|$))"
    
    date_time = None
    user = None
    message_text = None
    num_tokens = None

    def __init__(self, input_text) -> None:

        self.match_string(input_text)
        self.token_lenght(self.message_text)

    def match_string(self, input_text):

        match = re.match(self.pattern, input_text)

        if match:
            # Extracting groups from the match
            date_str, time_str, user, message_text = match.groups()

            # Replace non-breaking spaces with regular spaces in the user string
            user = user.replace("\xa0", " ")

            # Assigning the values
            self.user = user
            self.message_text = message_text.strip() if message_text else None

            # Parsing the combined date and time string into a datetime object
            datetime_str = date_str + ", " + time_str
            datetime_str = datetime_str.replace(".", "")  # Remove dots before parsing
            self.date_time = datetime.strptime(datetime_str, "%d%m%y, %I:%M:%S %p")
        else:
            print(f"ERROR in Line: {input_text}")

    def token_lenght(self, string):
        
        encoding = tiktoken.get_encoding("cl100k_base")
        try:
            self.num_tokens = len(encoding.encode(string))
        except:
            self.num_tokens = 0


class Txt_Reader():

    messages = []
    message_objs = []

    def __init__(self, path) -> None:

        self.read_file(path)
        self.convert_all()


    def read_file(self, path):

        # Open the text file
        with open(path, 'r', encoding='utf-8') as file:
            # Read the lines of the file
            lines = file.readlines()

        # Initialize an empty list to store the messages
        self.messages = []

        # Initialize an empty string to store the current message
        current_message = ''

        # Loop through each line in the file
        for line in lines:
            # Check if the line contains a message
            if line.startswith('['):
                # If there is a current message, add it to the messages list
                if current_message:
                    self.messages.append(current_message.strip())
                    current_message = ''
                # Add the new message to the current_message variable
                current_message += line.strip()
            else:
                # If the line does not start with '[', it's a continuation of the previous message
                # So, add it to the current_message variable
                current_message += '\n' + line.strip()

        # Add the last message to the messages list
        if current_message:
            self.messages.append(current_message.strip())

    def convert2message(self, string):
        return Message(string)
    
    def convert_all(self):

        for msg in self.messages:
            self.message_objs.append(self.convert2message(msg))

def split_messages(messages):
    max_tokens = 4000
    current_tokens = 0
    current_list = []
    result = []
    
    for message in messages:
        if current_tokens + message.num_tokens > max_tokens:
            # Ensure the last message in the current_list is from 🥀🌙
            for m in reversed(current_list):
                if m.user == '🥀🌙':
                    result.append(current_list)
                    current_list = []
                    current_tokens = 0
                    break
                else:
                    current_list.pop()  # Remove messages until we find one from 🥀🌙
        current_list.append(message)
        current_tokens += message.num_tokens
    
    # Combine consecutive messages from the same user
    for sublist in result:
        combined_list = []
        current_message = None
        for message in sublist:
            if current_message is None or current_message.user != message.user:
                if current_message is not None:
                    combined_list.append(current_message)
                current_message = message
            else:
                # Combine messages
                try:
                    current_message.message_text += '. ' + message.message_text
                except:
                    pass
                current_message.num_tokens += message.num_tokens
        # Append the last message
        if current_message is not None:
            combined_list.append(current_message)
        result[result.index(sublist)] = combined_list
    
    return result

def transform_to_dict(sublists):
    transformed_dict = {}
    for i, sublist in enumerate(sublists):
        conversation = []
        for message in sublist:
            if message.user == '🥀🌙':
                from_value = 'gpt'
            else:
                from_value = 'human'
            conversation.append({"from": from_value, "value": message.message_text})
        transformed_dict[i] = {"conversations": conversation}
    return transformed_dict     

def save_as_jsonl(transformed_dict, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for _, value in transformed_dict.items():
            json.dump(value, file, ensure_ascii=False)
            file.write('\n')

def merge_jsonl_files(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in glob.glob(os.path.join(directory, '*.jsonl')):
            with open(filename, 'r', encoding='utf-8') as infile:
                for line in infile:
                    outfile.write(line)


if __name__ == "__main__":

    import os
    import json

    #clean_folder("chats")
    
    for file in os.listdir("chats"):
        if file.endswith(".txt"):
            Txt = Txt_Reader(f"chats/{file}")
            sublists = split_messages(Txt.message_objs)
            message_dict = transform_to_dict(sublists)

            save_as_jsonl(message_dict, "data/output.jsonl")
            print(f"{file}: {Txt.message_objs.__len__()}")
    
    
    #merge_jsonl_files("data", "traindata.sjonl")
    
    