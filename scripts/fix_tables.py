import os
import glob

files = glob.glob('app/domain_models/*.py')
for file in files:
    if '__init__' in file:
        continue
    with open(file, 'r') as f:
        content = f.read()
    
    if '__table_args__' not in content:
        content = content.replace('__tablename__ = ', "__table_args__ = {'extend_existing': True}\n    __tablename__ = ")
        with open(file, 'w') as f:
            f.write(content)
