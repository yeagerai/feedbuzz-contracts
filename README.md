# FeedBuzz

FeedBuzz will be a decentralized feedback aggregation protocol, capable of gathering feedback and evaluating its validity and utility for application developers.

The first iteration of FeedBuzz will be used by MorAgents to verify, catalog and store user feedback, conversation logs and application errors in order to improve the Morpheus platform.

## Roadmap
### Phase 1: MVP
#### Description
- An instance of GenLayer will run by YeagerAI
    - FeedBuzz Intelligent Contracts running on it
- MorAgent instances send feedback to FeedBuzz by:
    - Identifying something to log
        - Due to error
        - Missing feature
        - Specific request by the user
    - Sanitizing the data 
    - Sending it to Genlayer
- Multiple LLM validators will evaluate whether the feedback being submitted is:
    - Correctly Signed
    - New, if not increment the count and point to original
    - A bug or a feature
    - Correctly formatted
    - Valid
    - Relevant
    - Which user sentiment - severity
- All information will be openly accessible through a web interface (FeedBuzz Explorer) as well as a MorAgent connected to an API
Estimated: August 2024


### Phase 2: Testnet
#### Description
- Intelligent Contract execution moved to a public test network
- All historical data is moved to testnet
- Other projects can release permissionless instances of FeedBuzz in order to gather feedback for any project
Estimated: November 2024


### Phase 3: Mainnet
#### Description
- Execution and data moves to mainnet
- Anti spam
- Account Abstraction can be used to cover the user’s gas cost
Estimated: March 2025

### Components
#### Genlayer Backend
- Missing Features:
    - Vector Embeddings
    - Signature checking
- Connect to Morpheus for inference
- Devops
    - Deployment
    - RPC
    - Spam prevention
Estimated: 6 weeks


#### FeedBuzz Intelligent Contracts
- Features: 
    - Accept logs from MorAgents instances
    - Filter invalid submissions and spam
    - Semantic duplicate detection
    - Categorize and curate feedback
Estimated: 1 Month

#### MorAgents to FeedBuzz connection
- Features:
    - Decide when to log
    - Sanitize the log
    - Submit log and user feedback to GenLayer
Estimated: 2 Weeks


#### FeedBuzz Explorer
- Features:
    - Browse aggregated logs and feedback
Estimated: 2 Weeks


### Future Ideas
- Possible to issue bounties for novel errors - decentralized QA
- Create bounties for features
- Submit additional feedback
- Vote on existing feedback


### Relevant Links
https://github.com/MorpheusAIs/moragents
https://github.com/yeagerai/genlayer-simulator/


### Development

Required to have the GenLayer simulator running
Run pyest to run the tests