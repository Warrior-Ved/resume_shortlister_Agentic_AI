"""
Quick test to check if Ollama is running and accessible
"""
import requests

def test_ollama():
    print("Testing Ollama connection...")

    try:
        # Test 1: Check if Ollama is running
        print("\n1. Checking if Ollama server is running...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("   ✅ Ollama is running!")
            models = response.json()
            print(f"   Available models: {[m['name'] for m in models.get('models', [])]}")
        else:
            print(f"   ❌ Ollama returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to Ollama!")
        print("   Please start Ollama: ollama serve")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

    try:
        # Test 2: Check if ministral model is available
        print("\n2. Checking if ministral model is available...")
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]

        ministral_model = None
        for name in model_names:
            if 'ministral' in name.lower():
                ministral_model = name
                break

        if ministral_model:
            print(f"   ✅ Ministral model found: {ministral_model}")
        else:
            print("   ❌ Ministral model not found!")
            print("   Available models:", model_names)
            print("   Please pull the model: ollama pull ministral-3:3b")
            return False
    except Exception as e:
        print(f"   ❌ Error checking models: {e}")
        return False

    try:
        # Test 3: Test a simple generation
        print("\n3. Testing model generation...")
        test_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": ministral_model,  # Use the found model name
                "prompt": "Say hello",
                "stream": False
            },
            timeout=30
        )

        if test_response.status_code == 200:
            result = test_response.json()
            print("   ✅ Model generation works!")
            print(f"   Response: {result.get('response', '')[:100]}...")
        else:
            print(f"   ❌ Generation failed with status: {test_response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error testing generation: {e}")
        return False

    print("\n✅ All tests passed! Ollama is working correctly.")
    return True

if __name__ == "__main__":
    success = test_ollama()
    if not success:
        print("\n⚠️  Please fix the issues above before running the resume shortlister.")
    else:
        print("\n🎉 You're ready to use the resume shortlister!")
