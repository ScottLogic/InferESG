@database_agent @ESG
Scenario Outline: When a user asks InferESG for information about their transaction history
    Given  a prompt to InferESG
    When   I get the response
    Then   the response to this '<prompt>' should match the '<expected_response>'
Examples:
|prompt                                                                         |expected_response      |
|Check the database and tell me the average ESG score (Environmental) for the WhiteRock ETF fund |The average ESG score (Environmental) for the WhiteRock ETF fund is approximately 69.67|
|Check the database and tell me the fund with the highest ESG social score        |Dynamic Industries with a score of 91|
|Check the database and tell me the fund with the lowest Governance ESG score     |Dynamic Industries, which has a score of 60|
# |Check the database and tell me the fund with the lowest ESG score                |Dynamic Industries with a score of 50|
# |Check the database and tell me the largest fund                                  |The largest fund is the Global Energy Fund, which has a size of 1,500|
# |Check the database and tell me which funds contain Shell                         |Funds containing Shell are European Growth Fund, Global Energy Fund, Silverman Global ETF and WhiteRock ETF|


@web_agent
Scenario Outline: When a user asks InferESG generic questions
    Given  a prompt to InferESG
    When   I get the response
    Then   the response to this '<prompt>' should match the '<expected_response>'
Examples:
|prompt                                             |expected_response  |
|What is the capital of France?                     |Paris              |
|What is the capital of Zimbabwe?                   |Harare             |
|What is the capital of Spain?                      |Madrid             |
|What is the capital of China?                      |Beijing            |
|What is the capital of United Kingdom?             |London             |
|What is the capital of Sweden?                     |Stockholm          |

@confidence
Scenario Outline: Check Response's confidence
    Given  a prompt to InferESG
    When   I get the response
    Then   the response to this '<prompt>' should give a confident answer
Examples:
|prompt                                                                     |
|What is the capital of France?                                             |

