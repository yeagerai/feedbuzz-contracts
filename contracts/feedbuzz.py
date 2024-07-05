import json
from genvm.base.icontract import IContract
from genvm.base.equivalence_principle import call_llm_with_principle


class FeedBuzz(IContract):
    def __init__(self):
        self.log_history = []

    async def submit_log(self, log: str) -> None:
        contains_failed_request_prompt = f"""
Analyze the given chat log of a conversation with an LLM-based agent. Determine if there was an unfulfilled request - a task the user asked for that the agent was unable to complete due to lacking capabilities. 

Respond with a JSON object containing a single boolean field named "unfulfilled_request".

Set "unfulfilled_request" to true if an unfulfilled request is found, and false if all requests were fulfilled or possible to fulfill.

Do not include any explanations or additional text outside the JSON object in your response.

Input: [{log}]

Output: 
{{"unfulfilled_request": true/false}}
"""
        llm_response = await call_llm_with_principle(
                contains_failed_request_prompt,
                eq_principle="Output has to match exactly",
            )
        contains_unfulfilled_request = json.loads(llm_response)["unfulfilled_request"]

        if not contains_unfulfilled_request:
            return "The chat log doesn't contain a failed request"
        
        extract_missing_capabilities_prompt = f"""
Examine the provided chat log of a conversation with an LLM-based agent. Identify any requests made by the user that the agent was unable to fulfill due to missing capabilities. Extract and list these missing features or capabilities in JSON format.

Input: [{log}]

Output: JSON array of missing features/capabilities, e.g.:
{{
  "missing_capabilities": [
    "real-time data access",
    "stock price prediction",
    "personalized financial advice"
  ]
}}

If no missing capabilities are identified, return an empty array.
"""
        llm_response = await call_llm_with_principle(
                extract_missing_capabilities_prompt,
                eq_principle="The provided list should contain all the missing features without being excessively duplicative. The identified features should have clear, concise titles",
                comparative=False,
            )
        missing_capabilites_list = json.loads(llm_response)

        id = self.log_history.append({
            "sender": contract_runner.from_address,
            "log": log,
            "missing_capabilities": missing_capabilites_list,
        })

        for missing_capability in missing_capabilites_list["missing_capabilities"]:
            print(f"Missing capability: {missing_capability}")
            # TODO: get closest capability form vector db
            # check if it's the same capability with LLM call
            # if not, create a new entry
            # add reference to log id

        return missing_capabilites_list

    def get_log_history(self):
        return self.log_history