#!/usr/bin/env python3
"""
Script to update .env file with HF_TOKEN
"""

import os

def update_env_file():
    """Add HF_TOKEN to .env file if not present"""
    env_file = ".env"
    
    # Read existing content
    content = ""
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
    
    # Check if HF_TOKEN already exists
    if "HF_TOKEN=" in content:
        print("HF_TOKEN already exists in .env file")
        return
    
    # Add HF_TOKEN and other required variables
    new_lines = [
        "HF_TOKEN=your_actual_huggingface_token_here",
        "AI_ENGINE=flux_working", 
        "DEVICE=cpu",
        "FLUX_MAX_GENERATIONS_PER_HOUR=10",
        "FLUX_MAX_GENERATIONS_PER_DAY=50", 
        "FLUX_COOLDOWN_SECONDS=30",
        ""
    ]
    
    with open(env_file, 'a') as f:
        f.write("\n" + "\n".join(new_lines))
    
    print("Added HF_TOKEN and other variables to .env file")
    print("Please replace 'your_actual_huggingface_token_here' with your actual token")

if __name__ == "__main__":
    update_env_file()
