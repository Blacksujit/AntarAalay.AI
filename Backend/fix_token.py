#!/usr/bin/env python3
"""
Fix the HF_TOKEN in .env file with the correct token
"""

import os

def fix_token():
    """Update .env file with the correct HF_TOKEN"""
    env_file = ".env"
    correct_token = "your_actual_huggingface_token_here"
    
    # Read existing content
    content = ""
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
    
    # Replace the HF_TOKEN line
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if line.startswith('HF_TOKEN='):
            new_lines.append(f'HF_TOKEN={correct_token}')
        else:
            new_lines.append(line)
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✅ Updated HF_TOKEN in .env file")
    print(f"Token: {correct_token[:10]}...{correct_token[-10:]}")

if __name__ == "__main__":
    fix_token()
