import os
import subprocess
import sys
import schedule
import time

# Path to the directory containing your scripts
script_dir = r'C:\Projects\01_NEWSSCRAP_MOFA'

# List of script files to execute
scripts = [
    '03_state_dept.py',
    '04_white_house.py',
    '07_dod_news.py',
    '09_mofa_news.py', 
    '10_mofa_notice.py', 
    '05_haitian_times.py',
    '06_haiti_libre.py',
    #'01_naver_news.py',
    '02_google_news.py',
    '11_mofa_latin.py'
]

# Virtual environment directory
venv_dir = os.path.join(script_dir, 'myenv')

# Function to create a virtual environment
def create_virtualenv():
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', venv_dir])

# Function to activate the virtual environment and install required packages
def setup_environment():
    if sys.platform == "win32":
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate.bat')
    else:
        activate_script = os.path.join(venv_dir, 'bin', 'activate')

    # Install required packages
    requirements = [
        'requests',
        'gnews',
        'schedule'
    ]

    # Activate the virtual environment and install packages
    for package in requirements:
        subprocess.run([os.path.join(venv_dir, 'Scripts', 'pip'), 'install', package])

# Function to run a script
def run_script(script_name):
    script_path = os.path.join(script_dir, script_name)
    result = subprocess.run([os.path.join(venv_dir, 'Scripts', 'python'), script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Script {script_name} executed successfully.")
    else:
        print(f"Error executing script {script_name}: {result.stderr}")

# Function to run all scripts
def run_all_scripts():
    for script in scripts:
        run_script(script)

# Schedule the task to run at 14:30 (2:30 PM) every day
schedule.every().day.at("09:04").do(run_all_scripts)

# Keep the script running
if __name__ == "__main__":
    create_virtualenv()
    setup_environment()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
