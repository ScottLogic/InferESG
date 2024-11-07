import_data_from_csv_script = """
LOAD CSV WITH HEADERS FROM 'file:///esg_poc.csv' AS row

MERGE (f:Fund {Name: row.`Fund Name`, Size: toFloat(row.`Fund Size (Billion USD)`)})

MERGE (c:Company {Name: row.`Company Name`})

MERGE (c)<-[:CONTAINS]-(f)

MERGE (i:Industry {Name: row.Industry})

MERGE (c)-[:BELONGS_IN_INDUSTRY]->(i)

MERGE (co:Country {Name: row.Country})

MERGE (c)-[:REGISTERED_IN]->(co)

MERGE (esge:ESGScore {
    Category: 'Environmental',
    Score: toFloat(row.`ESG score (Environmental)`),
    Date: row.`ESG scoring date`
})

MERGE (c)-[:HAS_ESG_SCORE]->(esge)

MERGE (esgs:ESGScore {
    Category: 'Social',
    Score: toFloat(row.`ESG score (Social)`),
    Date: row.`ESG scoring date`
})

MERGE (c)-[:HAS_ESG_SCORE]->(esgs)

MERGE (esgg:ESGScore {
    Category: 'Governance',
    Score: toFloat(row.`ESG score (Governance)`),
    Date: row.`ESG scoring date`
})

MERGE (c)-[:HAS_ESG_SCORE]->(esgg)
"""
