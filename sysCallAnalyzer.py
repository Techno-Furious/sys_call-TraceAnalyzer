
import subprocess
import sys
import google.generativeai as genai

genai.configure(api_key="API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

def interpret_logs(logs,command_argument):
    try:
        response = model.generate_content(f"You are an assistant that interprets syscall logs. Your output should only be the system call you see and explaining it in a line about it and at the end you try to guess what the command maybe or what the program maybe trying to do.I also can give you the command line input that was used to run this process, Here you go: {command_argument}, use this to guess the progrm, sometimes it can be a normal linux command, so this cli input that i have given you can be very helpful, you can make your guess sometimes just by looking at the command. Please analyze the following syscall logs and explain their meaning:\n{logs}")
        
        return response.text
    except Exception as e:
        print(f"Error interpreting logs: {e}")
        return "Error interpreting logs."

def read_logs(file_path):
    try:
        with open(file_path, 'r') as file:
            logs = file.read()
        return logs
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return ""
    except Exception as e:
        print(f"Error reading the file: {e}")
        return ""

def save_analysis(analysis, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(analysis)
        print(f"Analysis saved to {file_path}")
    except Exception as e:
        print(f"Error saving the analysis: {e}")

def main():
    if len(sys.argv) < 2:
        print("Please provide a command argument.")
        sys.exit(1)

    command_argument = sys.argv[1]
    result = subprocess.run(["./mytrace", command_argument], capture_output=True, text=True)
    print(result.stdout)

    logs = read_logs("syscallLogs.txt")
    if not logs:
        print("No logs found. Exiting.")
        return
    
    analysis = interpret_logs(logs,command_argument)
    save_analysis(analysis, "analysis.txt")

if __name__ == "__main__":
    main()

