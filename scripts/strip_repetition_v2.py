import os
import glob
import re

# 2. Strip massive dummy CSS from templates
html_files = glob.glob('app/templates/domain/*.html')
for file in html_files:
    with open(file, 'r') as f:
        content = f.read()
    
    # Remove everything from <style> to </style>
    stripped_content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
    
    with open(file, 'w') as f:
        f.write(stripped_content)

# 3. Strip repetitive attribute columns from models
model_files = glob.glob('app/domain_models/*.py')
for file in model_files:
    with open(file, 'r') as f:
        lines = f.readlines()
    
    # Keep lines that do not define dummy 'attribute_' columns
    clean_lines = [line for line in lines if 'attribute_' not in line]
    
    with open(file, 'w') as f:
        f.writelines(clean_lines)

# 4. Strip repetitive tests
test_files = glob.glob('tests/**/*.py', recursive=True)
for file in test_files:
    with open(file, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    clean_lines = []
    skip = False
    for line in lines:
        if line.startswith('def test_'):
            if 'attribute_' in line or 'edge_case_' in line or 'error_handling_case_' in line:
                skip = True
            else:
                skip = False
        
        if not skip:
            clean_lines.append(line)
            
    with open(file, 'w') as f:
        f.write('\n'.join(clean_lines))

import zipfile
project_dir = r"c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus"
zip_path = r"c:\Users\saiku\OneDrive\Desktop\dataflow_nexus_organic.zip"
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

print(f"Cleaned project zipped to: {zip_path}")
