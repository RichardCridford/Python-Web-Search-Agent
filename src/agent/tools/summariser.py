# summariser.py

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from openai import OpenAI

# Create a single shared OpenAI client instance
client = OpenAI()


class SummariserInput(BaseModel):
    """Input schema for the summariser tool."""
    # The user must attach a description, there is no default, lets you add extra information to each attribute in a model 
    # (in this case the description)
    text: str = Field(..., description="The raw text to summarise.")
    # Max points must be an integer, if no value provided default to 5
    max_points: int = Field(5, description="Maximum number of bullet points to return.")


class SummariserOutput(BaseModel):
    """Output schema for the summariser tool."""
    summary: List[str] = Field(..., description="List of concise bullet points summarising the text.")


class SummariserTool:
    """
    A tool that uses an LLM to summarise text into concise bullet points.
    Designed to be used inside an agent/tool ecosystem.
    """

    name = "summariser"
    description = "Summarises raw text into concise bullet points using an LLM."
    input_model = SummariserInput
    output_model = SummariserOutput


    def run(self, text: str, max_points: int = 5) -> Dict[str, Any]:
        """
        Summarise the given text using an LLM.

        Args:
            text (str): The raw text to summarise.
            max_points (int): Maximum number of bullet points to return.

        Returns:
            Dict[str, Any]: A dictionary matching SummariserOutput.
        """

        prompt = (
            "Summarise the following text into concise bullet points. "
            "Focus on clarity, key facts, and essential information. "
            f"Return no more than {max_points} bullet points.\n\n"
            f"Text:\n{text}\n\n"
            "Return ONLY the bullet points, one per line, no numbering."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            raw_output = response.choices[0].message["content"]
            lines = raw_output.strip().split("\n")


            # Clean bullet points
            cleaned = [
                line.lstrip("-• ").strip()
                for line in lines
                if line.strip()
            ]


            return SummariserOutput(summary=cleaned[:max_points]).model_dump()

        except Exception as e:
            # Fail gracefully — tools should never crash the agent
            return SummariserOutput(
                summary=[f"Summarisation failed: {str(e)}"]
            ).model_dump()






