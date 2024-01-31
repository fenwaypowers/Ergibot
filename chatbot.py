import paramiko
import globals
import os, subprocess


class Chatbot:
    '''
    Abstract class for Chatbot. 
    '''

    msg: str
    user: str
    full_msg: str
    command: str

    def __init__(self):
        pass

    def get_reply(self):
        return "`get_reply` not implemented."
    
class LocalChatbot(Chatbot):
    """
    Not implemented yet.
    """
    pass

class ServerChatbot(Chatbot):
    def __init__(self, user:str, msg: str):
        self.msg = msg
        self.user = user
        self.full_msg = f"username: {user} message: {self.msg}"
        self.command = globals.config.chatbot.command
    
    def get_reply(self, model: str = globals.config.chatbot.default_model):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(globals.config.chatbot.ip,
            username=globals.config.chatbot.username,
            password=globals.config.chatbot.password)

            self.command += f" --model {model}"

            client.exec_command(f"echo \"{self.full_msg}\" > msg.txt")
            print(f"Executing command on {globals.config.chatbot.ip}:", self.command)
            stdin, stdout, stderr = client.exec_command(self.command)

            # Read the output
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if output:
                return f"prompt: `{self.msg}`\n{output}"
            if error:
                print("Error: " + error)
                return "Error. Something went wrong"
            return f"Error. Something went wrong."
        except Exception as e:
            print("SSH connection or command execution failed:", e)
            return "Connection or execution failed."
        finally:
            client.close()        
