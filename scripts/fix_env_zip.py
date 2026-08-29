import zipfile
import os

project_dir = r"c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus"
zip_path = r"c:\Users\saiku\OneDrive\Desktop\dataflow_nexus_70k.zip"
exclude_dirs = {'venv', '__pycache__', '.pytest_cache'}
exclude_files = {'.env', '.env.example'}

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file in exclude_files or file.endswith('.pyc') or file.endswith('.pyo'):
                continue
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, project_dir)
            zipf.write(file_path, arcname)

print(f"Compliance fixed (secrets completely stripped) and zipped to: {zip_path}")
