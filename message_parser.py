import re
from datetime import datetime

class Message():
    # Regular expression pattern to match date, time, username/number, and message text
    pattern = r"\[(\d{2}\.\d{2}\.\d{2}), (\d{1,2}:\d{2}:\d{2} (?:AM|PM))\] (.+?): (.+)"
    
    date_time = None
    user = None
    message_text = None

    def __init__(self, input_text) -> None:
        match = re.match(self.pattern, input_text)

        if match:
            # Extracting groups from the match
            date_str, time_str, self.user, self.message_text = match.groups()

            # Parsing the combined date and time string into a datetime object
            datetime_str = date_str + ", " + time_str
            self.date_time = datetime.strptime(datetime_str, "%d.%m.%y, %I:%M:%S %p")
        else:
            print(f"ERROR in Line: {input_text}")

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

        


if __name__ == "__main__":

    import os
    
    for file in os.listdir("chats"):
        if file.endswith(".txt"):
            Txt = Txt_Reader(f"chats/{file}")
            print(f"{file}: {Txt.message_objs.__len__()}")
    
    