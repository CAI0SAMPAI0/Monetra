import os
import glob

def run():
    # Find all HTML files in frontend and the common.js file
    files = glob.glob('frontend/**/*.html', recursive=True) + ['frontend/static/js/common.js']

    for filepath in files:
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace relative static paths with absolute ones
            new_content = content.replace('href="static/', 'href="/static/')
            new_content = new_content.replace('src="static/', 'src="/static/')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated: {filepath}")

if __name__ == '__main__':
    run()
