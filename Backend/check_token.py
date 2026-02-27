#!/usr/bin/env python3
"""Check the actual HF_TOKEN being loaded"""

from app.config import get_settings

def check_token():
    settings = get_settings()
    token = settings.HF_TOKEN
    
    print(f"HF_TOKEN loaded: {'✅' if token else '❌'}")
    print(f"Token length: {len(token) if token else 0}")
    if token:
        print(f"Token starts with: {token[:10]}...")
        print(f"Token ends with: ...{token[-10:]}")
        
        # Check if it looks like a valid HF token
        if token.startswith("hf_"):
            print("✅ Token format looks correct (starts with hf_)")
        else:
            print("❌ Token format incorrect - should start with hf_")
            
        if len(token) < 30:
            print("❌ Token too short - HF tokens are usually longer")
        else:
            print("✅ Token length looks correct")
    else:
        print("❌ No token found")

if __name__ == "__main__":
    check_token()
