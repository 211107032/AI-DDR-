import glob

for f in glob.glob('*.py'):
    if f == 'fix.py': continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace literal \"\"\" with """
    content = content.replace('\\"\\"\\"', '\"\"\"')
    # Replace literal \\n with \n
    content = content.replace('\\\\n', '\\n')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Fixed files.")
