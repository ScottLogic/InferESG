@transaction_history @spending
Scenario Outline: When a user asks InferESG for information about their transaction history
    Given  a prompt to InferESG
    When   I get the response
    Then   the response to this '<prompt>' should match the '<expected_response>'
Examples:
|prompt                                                                         |expected_response      |
# |How much did I spend at Tesco?                                                 |639.84|
|Check the database and tell me the fund with the highest ESG social score        |The average ESG score (Environmental) for the WhiteRock ETF fund is approximately 69.67.|

# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|
# |How much did I spend at Tesco?                                                 |639.84|

# |How much did I spend on Amazon?                                                |You spent a total of £1586.56 on Amazon    |
# |How much did I spend on Tesco compared to Amazon?                              |946.72                 |

@generic
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
|How much did I spend at Tesco?                                             |

