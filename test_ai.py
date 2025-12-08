"""Test AI mode functionality"""
from src.engine import ResumeEngine, AI_AVAILABLE

print(f"AI Available: {AI_AVAILABLE}")

if AI_AVAILABLE:
    e = ResumeEngine()
    print("Testing AI mode...")
    
    data = {
        'name': 'Test User',
        'email': 'test@test.com',
        'phone': '123-456-7890',
        'education': 'BS Computer Science',
        'skills': 'Python, JavaScript, Problem Solving',
        'experience': 'Software Developer\nTech Corp\nBuilt web applications'
    }
    
    print("\nGenerating with AI mode...")
    result = e.generate_resume(data, 'ai')
    print(f"\nGenerated {len(result)} characters")
    print("\nFirst 300 characters:")
    print(result[:300])
    print("\n✅ AI mode test complete!")
else:
    print("❌ AI not available - transformers package not installed")
    print("Install with: pip install transformers torch")

