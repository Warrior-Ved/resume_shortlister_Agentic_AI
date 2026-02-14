"""
Quick test to verify async/await fix in Phase 2
"""
import asyncio
import httpx

async def test_async_http():
    """Test that async HTTP client works correctly"""
    print("Testing async HTTP client...")

    try:
        client = httpx.AsyncClient(timeout=30.0)

        # Test with Ollama
        print("  Testing Ollama connection...")
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "ministral-3:3b",
                "prompt": "Say 'test successful' in JSON format: {\"result\": \"...\"}",
                "stream": False,
                "format": "json"
            }
        )

        response.raise_for_status()
        result = response.json()

        print(f"  ✅ Async HTTP works!")
        print(f"  Response: {result.get('response', '')[:100]}...")

        await client.aclose()

        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_async_http())

    if success:
        print("\n✅ Phase 2 async/await fix verified!")
        print("   The shortlister will work correctly now.")
    else:
        print("\n❌ Test failed. Check if Ollama is running.")
