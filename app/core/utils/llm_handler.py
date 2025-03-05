from litellm import acompletion


class LLMHandler:
    """
    A handler class for interacting with Large Language Models (LLMs) using litellm.
    Provides methods to make asynchronous calls to LLM APIs.
    """

    @staticmethod
    async def call_llm(system_prompt: str, user_prompt: str, model: str = "gpt-4o-mini", response_format: dict = None, temperature: float = 0.0):
        """
        Asynchronously generates a response from the LLM using the provided system and user prompts.
        
        Args:
            system_prompt (str): The system instructions for the LLM that define its behavior
            user_prompt (str): The user's input or query to the LLM
            model (str, optional): The LLM model to use. Defaults to "gpt-4o-mini".
            response_format (dict, optional): Format specification for the response. Defaults to None.
            temperature (float, optional): Controls randomness in the output. Lower values make output more deterministic. Defaults to 0.0.
            
        Returns:
            str: The generated text response from the LLM
        """
        # Prepare the messages in the format expected by the LLM API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Make the asynchronous API call to the LLM
        response = await acompletion(
            model=model,
            temperature=temperature,
            response_format=response_format,
            messages=messages
        )
        
        # Extract and return just the content from the response
        # The full response contains additional metadata we don't need
        return response.choices[0].message.content
