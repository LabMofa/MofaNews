import os
import subprocess
import sys

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

# List of required packages
required_packages = [
    'requests',
    'gnews',
    'schedule'
]

# Function to install required packages
def install_packages(packages):
    for package in packages:
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)

# Function to run a script
def run_script(script_name):
    script_path = os.path.join(script_dir, script_name)
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Script {script_name} executed successfully.")
    else:
        print(f"Error executing script {script_name}: {result.stderr}")

# Function to run all scripts
def run_all_scripts():
    for script in scripts:
        run_script(script)

# Run all scripts
if __name__ == "__main__":
    install_packages(required_packages)
    run_all_scripts()
