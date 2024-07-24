import json
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import call_llm_with_principle


class FeedBuzz(IContract):
    def __init__(self):
        self.log_history = {}
        self.next_log_id = 0
        self.vector_store = VectorStore()

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

        print(llm_response)
        missing_capabilities_list = json.loads(llm_response)

        log_id = self.next_log_id
        self.next_log_id += 1

        self.log_history[log_id] = {
            "sender": contract_runner.from_address,
            "log": log,
            "missing_capabilities": missing_capabilities_list,
        }

        for missing_capability in missing_capabilities_list["missing_capabilities"]:
            print(f"Missing capability: {missing_capability}")

            result = self.vector_store.get_closest_vector(missing_capability)

            is_duplicate = False
            if result is not None:
                similarity, capability_id, existing_capability, metadata, _ = result

                print(f"Existing capability: {existing_capability}")
                print(f"Similarity: {similarity}")
                print(f"Capability ID: {capability_id}")
                print(f"Metadata: {metadata}")
            
                if similarity > 0.99:
                    is_duplicate = True
                elif similarity > 0.9:
                    deduplicate_capabilities_prompt = f"""
Following are two capabilities extracted from chat logs:
            
Existing capability: {existing_capability}
Missing capability: {missing_capability}

Determine if the two capabilities are the same, and can be merged, or if they are different.

Output: JSON object:
{{
    "is_duplicate": true/false
}}
        """            
                    llm_response = await call_llm_with_principle(
                        deduplicate_capabilities_prompt,
                        eq_principle="Output has to match exactly",
                        comparative=True,
                    )

                    is_duplicate = json.loads(llm_response)["is_duplicate"]
            
            if is_duplicate:
                metadata["log_ids"].append(log_id)
                self.vector_store.update_text(capability_id, existing_capability, metadata)
            else:
                self.vector_store.add_text(missing_capability, {"log_ids": [log_id]})

        return missing_capabilities_list

    def get_log_history(self):
        return self.log_history

    def get_missing_capabilities(self):
        return self.vector_store.get_all_items()