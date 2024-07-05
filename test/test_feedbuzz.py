# tests/e2e/test_wizard_of_coin.py

from tools.request import (
    payload,
    post_request_localhost,
    post_request_and_wait_for_finalization,
)
from tools.structure import execute_icontract_function_response_structure
from tools.response import (
    assert_dict_struct,
    has_success_status,
)


def test_feedbuzz():
    # Validators
    result = post_request_localhost(
        payload("create_random_validators", 10, 8, 12, ["openai"])
    ).json()
    assert has_success_status(result)

    # Account
    result = post_request_localhost(payload("create_account")).json()
    assert has_success_status(result)
    assert "account_address" in result["result"]["data"]
    from_address = result["result"]["data"]["account_address"]
    result = post_request_localhost(payload("fund_account", from_address, 10)).json()
    assert has_success_status(result)

    # Deploy Contract
    contract_code = open("contracts/feedbuzz.py", "r").read()
    data = [
        from_address,  # from_account
        "FeedBuzz",  # class_name
        contract_code,  # contract_code
        '',  # constructor
    ]
    call_method_response_deploy, transaction_response_deploy = (
        post_request_and_wait_for_finalization(
            payload("deploy_intelligent_contract", *data)
        )
    )

    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    # Execute Contract
    function = "submit_log"
    args = ["""
  {
    "content": "Can you tell me which stock to buy tomorrow based on the content of the news tomorrow morning?",
    "role": "user"
  },
  {
    "content": "I apologize for any confusion, but I can't provide real-time information or make investment recommendations. However, I can suggest a general approach to making investment decisions:\n\n1. **Research and Analysis**: Before making any investment, it's crucial to conduct thorough research on the company, industry, and market trends. Look at financial statements, news articles, and analyst reports.\n\n2. **Diversification**: Spread your investments across different asset classes (stocks, bonds, real estate) and industries to reduce risk.\n\n3. **Long-Term Perspective**: Invest for the long term. Short-term market fluctuations should not dictate your investment decisions.\n\n4. **Consult a Financial Advisor**: If you're unsure about which stock to buy or need guidance on your investment strategy, consider consulting with a financial advisor who can provide personalized advice based on your specific circumstances and goals.\n\n5. **Stay Informed**: Keep up-to-date with the latest news and developments in the market and industry you're interested in.\n\nRemember, investing always comes with risks, so it's essential to do thorough research and consider seeking professional advice before making any investment decisions.",
    "role": "assistant"
  }
"""]
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function", from_address, contract_address, function, args
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert format
    assert_dict_struct(
        transaction_response_call_1, execute_icontract_function_response_structure
    )
