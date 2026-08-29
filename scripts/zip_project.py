import os
import zipfile

project_dir = r"c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus"
zip_path = r"c:\Users\saiku\OneDrive\Desktop\dataflow_nexus_enterprise.zip"

exclude_dirs = {'venv', '.git', '__pycache__', '.pytest_cache'}

def should_exclude(dirpath):
    parts = dirpath.replace(project_dir, '').split(os.sep)
    return any(ex in parts for ex in exclude_dirs)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_dir):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                continue
            
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, project_dir)
            zipf.write(file_path, arcname)

print(f"Project successfully zipped to: {zip_path}")
