import requests
import json
from typing import Dict, Optional

def extract_investor_info(text: str) -> Dict[str, Optional[str]]:
    """
    Uses Ollama's Mistral to extract structured data from unstructured text.
    Returns a dictionary with: age, budget, start_date, end_date, avoid, salary.
    """
    # Define required fields with default None values
    required_fields = ["age", "budget", "start_date", "end_date", "avoid", "salary"]
    
    # Enhanced prompt with clearer instructions
    prompt = f"""Analyze this text and extract the following details as a valid JSON object:
{{
    "age": <integer>,
    "budget": <integer without $ or commas>,
    "start_date": <YYYY-MM-DD>,
    "end_date": <YYYY-MM-DD>,
    "avoid": <text description>,
    "salary": <integer if present>
}}

Text to analyze: "{text}"

Return ONLY the JSON object between ```json markers, nothing else."""

    try:
        # Verify Ollama is running first
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()

        # Send the request to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.3}  # Less creative, more factual
            },
            timeout=30
        )
        response.raise_for_status()

        # Extract and clean the JSON response
        llm_output = response.json()
        raw_response = llm_output["response"].strip()
        
        # Handle different response formats
        if "```json" in raw_response:
            json_str = raw_response.split("```json")[1].split("```")[0]
        else:
            json_str = raw_response[raw_response.find("{"):raw_response.rfind("}")+1]

        # Parse and validate the JSON
        result = json.loads(json_str)
        
        # Ensure all required fields are present
        return {field: result.get(field) for field in required_fields}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {field: None for field in required_fields}

