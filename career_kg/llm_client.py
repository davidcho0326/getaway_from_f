"""
Career KG — LLM Client
- Text generation: Claude Opus 4.6 (claude-opus-4-6)
- Vector embeddings: Gemini text-embedding-004 (768 dim)
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import anthropic
import google.generativeai as genai

# Load .env: career_kg/.env first, then parent venv/.env for API keys
load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")


class LLMClient:
    """Dual LLM wrapper: Claude for generation, Gemini for embeddings."""

    def __init__(self):
        # Claude Opus 4.6
        api_key = os.getenv("antrophic_API_key")
        if not api_key:
            raise ValueError("antrophic_API_key not found in .env")
        self.claude = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-opus-4-6"

        # Gemini embeddings
        gemini_key = os.getenv("GOOGLE_API_KEY")
        if not gemini_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")
        genai.configure(api_key=gemini_key)

    def generate_response(self, prompt: str, system_instruction: str = None, max_tokens: int = 16384) -> str:
        """Generate text with Claude Opus 4.6."""
        try:
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }
            if system_instruction:
                kwargs["system"] = system_instruction
            response = self.claude.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            return f"Error generating response: {e}"

    def get_embedding(self, text: str) -> list[float]:
        """Generate 768-dim embedding with Gemini gemini-embedding-001."""
        try:
            result = genai.embed_content(
                model="models/gemini-embedding-001",
                content=text,
                task_type="retrieval_document",
                output_dimensionality=768,
            )
            return result["embedding"]
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []


if __name__ == "__main__":
    client = LLMClient()
    print(client.generate_response("Say hello in one sentence."))
    emb = client.get_embedding("test embedding")
    print(f"Embedding dim: {len(emb)}")
