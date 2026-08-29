import os
import subprocess
import zipfile

project_dir = r"c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus"
os.chdir(project_dir)

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=False)

# 1. Rename .env.example to example.env
if os.path.exists(".env.example"):
    os.rename(".env.example", "example.env")
    run_cmd('git rm --cached .env.example')
    run_cmd('git rm .env.example')

# 2. Ensure .env is completely removed from git
run_cmd('git rm --cached .env')

# 3. Update .gitignore
with open('.gitignore', 'w') as f:
    f.write(".env\n.env.*\nvenv/\n__pycache__/\n*.pyc\n")

# 4. Commit the changes
run_cmd('git add .gitignore example.env')
run_cmd('git commit -m "chore: remove all .env files and use example.env instead"')

# 5. Re-zip the 70k project
zip_path = r"c:\Users\saiku\OneDrive\Desktop\dataflow_nexus_70k.zip"
exclude_dirs = {'venv', '__pycache__', '.pytest_cache'}

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                continue
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, project_dir)
            zipf.write(file_path, arcname)

print(f"Compliance fixed and zipped to: {zip_path}")
