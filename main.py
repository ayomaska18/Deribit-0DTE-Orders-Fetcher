import subprocess
import concurrent.futures
import os
import sys

def run_script(script_name):
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script_name}: {result.stderr}")
    else:
        print(f"Successfully ran {script_name}")

def main():
    scripts = [
        'GET_0DTE_POSITION_DATA_SOL.PY',
        'GET_0DTE_POSITION_DATA_ETH.PY',
        'GET_0DTE_POSITION_DATA_BTC.PY'
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_script, script) for script in scripts]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Run get_summary.py after fetching data
    run_script('get_summary.py')

if __name__ == "__main__":
    main()