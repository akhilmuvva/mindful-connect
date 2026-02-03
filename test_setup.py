"""
Test script to verify environment setup
Run this before starting the main app
"""

import sys
from pathlib import Path

def test_environment():
    """Test if environment is properly configured"""
    
    print("[*] Testing Mindful Connect Environment...\n")
    
    issues = []
    warnings = []
    
    # Test 1: Check Python version
    print("[OK] Python Version:", sys.version.split()[0])
    
    # Test 2: Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("[OK] .env file found")
        
        # Read and check for placeholder values
        with open(env_file, 'r') as f:
            content = f.read()
            
            if "sk-proj-xxxxx" in content or "OPENAI_API_KEY=sk-proj-xxxxx" in content:
                issues.append("[FAIL] OpenAI API key not configured in .env")
            else:
                print("[OK] OpenAI API key appears to be set")
            
            if "your-project-id" in content or "FIREBASE_PROJECT_ID=your-project-id" in content:
                issues.append("[FAIL] Firebase project ID not configured in .env")
            else:
                print("[OK] Firebase project ID appears to be set")
                
    else:
        issues.append("[FAIL] .env file not found")
    
    # Test 3: Check serviceAccountKey.json
    service_key = Path("serviceAccountKey.json")
    if service_key.exists():
        print("[OK] serviceAccountKey.json found")
    else:
        issues.append("[FAIL] serviceAccountKey.json not found")
    
    # Test 4: Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("[OK] Virtual environment activated")
    else:
        warnings.append("[WARN] Virtual environment may not be activated")
    
    # Test 5: Check core dependencies
    print("\n[*] Checking dependencies...")
    
    dependencies = {
        'streamlit': 'Streamlit UI framework',
        'openai': 'OpenAI API client',
        'firebase_admin': 'Firebase Admin SDK',
        'transformers': 'Hugging Face Transformers',
        'torch': 'PyTorch',
        'plotly': 'Plotly visualization'
    }
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"  [OK] {package} - {description}")
        except ImportError:
            issues.append(f"[FAIL] Missing package: {package}")
    
    # Print results
    print("\n" + "="*60)
    
    if not issues and not warnings:
        print("[SUCCESS] ALL CHECKS PASSED!")
        print("\n[RUN] You're ready to run the app:")
        print("   streamlit run src/app.py")
        return True
    else:
        if warnings:
            print("\n[WARNINGS]:")
            for warning in warnings:
                print(f"  {warning}")
        
        if issues:
            print("\n[ISSUES FOUND]:")
            for issue in issues:
                print(f"  {issue}")
            
            print("\n[INFO] Please follow SETUP_NOW.md to fix these issues")
            return False
    
    print("="*60)
    return len(issues) == 0

if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1)
