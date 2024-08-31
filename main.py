import os
import shutil
import ollama

def get_folder_for_file(file_name, folders):
    prompt = (
        f"There are {len(folders)} folders called {', '.join(folders)}. "
        f"Which folder would the file '{file_name}' go into? Short response please."
    )
    
    stream = ollama.chat(
        model='qwen2:1.5b',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True
    )

    response_content = ""
    for chunk in stream:
        response_content += chunk['message']['content']
    
    print(f"Response for {file_name}: {response_content}")
    
    for folder in folders:
        if folder in response_content:
            return folder
    
    return None

def organize_files(directory):
    folders = [f for f in os.listdir(directory) 
               if os.path.isdir(os.path.join(directory, f)) and f != 'qwen1']
    
    files = [f for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f)) and f != 'main.py']
    
    print(f"Folders: {folders}")
    print(f"Files: {files}")

    for file in files:
        target_folder = get_folder_for_file(file, folders)
        if target_folder:
            source_path = os.path.join(directory, file)
            target_path = os.path.join(directory, target_folder, file)
            
            shutil.move(source_path, target_path)
            print(f"Moved {file} to {target_folder}")
        else:
            print(f"Could not determine a folder for {file}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    organize_files(current_directory)
