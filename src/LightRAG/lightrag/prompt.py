from __future__ import annotations

from typing import Any

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

# PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event", "category"]
PROMPTS["DEFAULT_ENTITY_TYPES"] = [
    "durian_variety",
    "pest",
    "disease",
    "farming_practice",
    "location",
    "expert",
    "organization",
]

PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

PROMPTS["entity_extraction"] = """---Goal---
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

---Steps---
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: [{entity_types}]
Text:
{input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [durian_variety, pest, disease, farming_practice, location, expert, organization]
Text:
```
In Chanthaburi province, the heart of durian production in Thailand, farmers face challenges from pests like the durian seed borer. This insect lays eggs inside the durian fruit, causing significant damage. To combat this, the Department of Agriculture recommends integrated pest management (IPM) strategies, including the use of pheromone traps and biological controls.

One effective biological control is the introduction of parasitic wasps that target the durian seed borer larvae. Additionally, maintaining farm hygiene by removing fallen fruits can reduce pest populations.

Farmers in Chanthaburi have reported success with these methods, leading to healthier durian trees and higher quality fruit.
```

Output:
("entity"{tuple_delimiter}"Chanthaburi"{tuple_delimiter}"location"{tuple_delimiter}"Chanthaburi is a province in Thailand known for durian production."){record_delimiter}
("entity"{tuple_delimiter}"durian seed borer"{tuple_delimiter}"pest"{tuple_delimiter}"The durian seed borer is an insect pest that damages durian fruits by laying eggs inside them."){record_delimiter}
("entity"{tuple_delimiter}"Department of Agriculture"{tuple_delimiter}"organization"{tuple_delimiter}"The Department of Agriculture is a government body providing recommendations for pest management in agriculture."){record_delimiter}
("entity"{tuple_delimiter}"integrated pest management"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Integrated pest management (IPM) is a strategy that combines multiple approaches to control pests effectively."){record_delimiter}
("entity"{tuple_delimiter}"pheromone traps"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Pheromone traps are devices used to attract and capture pests like the durian seed borer."){record_delimiter}
("entity"{tuple_delimiter}"parasitic wasps"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Parasitic wasps are biological control agents that target pest larvae, such as those of the durian seed borer."){record_delimiter}
("entity"{tuple_delimiter}"farm hygiene"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Farm hygiene involves practices like removing fallen fruits to reduce pest populations."){record_delimiter}
("relationship"{tuple_delimiter}"durian seed borer"{tuple_delimiter}"Chanthaburi"{tuple_delimiter}"The durian seed borer is a significant pest in durian farms located in Chanthaburi."{tuple_delimiter}"pest impact, regional agriculture"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Department of Agriculture"{tuple_delimiter}"integrated pest management"{tuple_delimiter}"The Department of Agriculture recommends integrated pest management strategies to control pests like the durian seed borer."{tuple_delimiter}"pest control recommendation, agricultural policy"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"integrated pest management"{tuple_delimiter}"pheromone traps"{tuple_delimiter}"Integrated pest management includes the use of pheromone traps as a control method."{tuple_delimiter}"pest control technique, strategy component"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"integrated pest management"{tuple_delimiter}"parasitic wasps"{tuple_delimiter}"Integrated pest management incorporates biological controls like parasitic wasps."{tuple_delimiter}"biological control, pest management"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"integrated pest management"{tuple_delimiter}"farm hygiene"{tuple_delimiter}"Integrated pest management emphasizes farm hygiene practices to reduce pest populations."{tuple_delimiter}"preventive measure, pest control"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"parasitic wasps"{tuple_delimiter}"durian seed borer"{tuple_delimiter}"Parasitic wasps target the larvae of the durian seed borer, helping to control its population."{tuple_delimiter}"biological control, pest management"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"durian farming, pest management, integrated pest management, biological control, farm hygiene"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [durian_variety, pest, disease, farming_practice, location, expert, organization]
Text:
```
The durian market in Southeast Asia has seen significant growth, with prices for premium varieties like Musang King reaching record highs. In Malaysia, the Musang King durian fetched prices up to RM100 per kilogram during the peak season. This surge is attributed to increasing demand from China and other export markets.

To support durian farmers, the Malaysian government has introduced subsidies for fertilizers and pesticides. Additionally, the Durian Exporters Association has been promoting sustainable farming practices to ensure long-term viability.

However, challenges remain, such as the threat of durian diseases like Phytophthora, which can devastate orchards if not managed properly.
```

Output:
("entity"{tuple_delimiter}"Musang King"{tuple_delimiter}"durian_variety"{tuple_delimiter}"Musang King is a premium durian variety known for its high market value."){record_delimiter}
("entity"{tuple_delimiter}"Malaysia"{tuple_delimiter}"location"{tuple_delimiter}"Malaysia is a major producer of durian, particularly the Musang King variety."){record_delimiter}
("entity"{tuple_delimiter}"China"{tuple_delimiter}"location"{tuple_delimiter}"China is a significant export market for durian, driving demand and prices."){record_delimiter}
("entity"{tuple_delimiter}"Malaysian government"{tuple_delimiter}"organization"{tuple_delimiter}"The Malaysian government supports durian farmers through subsidies for agricultural inputs."){record_delimiter}
("entity"{tuple_delimiter}"Durian Exporters Association"{tuple_delimiter}"organization"{tuple_delimiter}"The Durian Exporters Association promotes sustainable farming practices among durian farmers."){record_delimiter}
("entity"{tuple_delimiter}"Phytophthora"{tuple_delimiter}"disease"{tuple_delimiter}"Phytophthora is a disease that can severely affect durian orchards if not managed."){record_delimiter}
("entity"{tuple_delimiter}"fertilizers"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Fertilizers are agricultural inputs used to enhance soil fertility and durian tree growth."){record_delimiter}
("entity"{tuple_delimiter}"pesticides"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Pesticides are chemicals used to control pests in durian farming."){record_delimiter}
("entity"{tuple_delimiter}"sustainable farming practices"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Sustainable farming practices aim to maintain long-term productivity and environmental health in durian farming."){record_delimiter}
("relationship"{tuple_delimiter}"Musang King"{tuple_delimiter}"Malaysia"{tuple_delimiter}"Musang King is primarily grown in Malaysia, contributing to its reputation as a durian hub."{tuple_delimiter}"regional specialty, agricultural production"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Musang King"{tuple_delimiter}"China"{tuple_delimiter}"High demand from China has led to increased prices for Musang King durian."{tuple_delimiter}"market demand, price influence"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Malaysian government"{tuple_delimiter}"fertilizers"{tuple_delimiter}"The Malaysian government provides subsidies for fertilizers to support durian farmers."{tuple_delimiter}"agricultural support, input subsidy"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Malaysian government"{tuple_delimiter}"pesticides"{tuple_delimiter}"The Malaysian government also subsidizes pesticides for durian farmers."{tuple_delimiter}"agricultural support, input subsidy"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Durian Exporters Association"{tuple_delimiter}"sustainable farming practices"{tuple_delimiter}"The Durian Exporters Association encourages the adoption of sustainable farming practices."{tuple_delimiter}"sustainability promotion, industry initiative"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Phytophthora"{tuple_delimiter}"durian orchards"{tuple_delimiter}"Phytophthora poses a significant threat to durian orchards, requiring careful management."{tuple_delimiter}"disease impact, orchard health"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"durian market, export demand, government subsidies, sustainable practices, disease management"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [durian_variety, pest, disease, farming_practice, location, expert, organization]
Text:
```
In Rayong, Thailand, farmer Anuwat has developed an innovative pruning technique that increases the yield of Monthong durian trees. By carefully timing the pruning and using organic fertilizers, he has achieved yields significantly higher than the regional average.

His methods have been studied by researchers from Kasetsart University, who are also investigating solutions for durian root rot, a disease prevalent in the area.

The Thai Durian Growers Association has recognized Anuwat's contributions and is promoting his techniques to other farmers.
```

Output:
("entity"{tuple_delimiter}"Rayong"{tuple_delimiter}"location"{tuple_delimiter}"Rayong is a province in Thailand known for durian farming."){record_delimiter}
("entity"{tuple_delimiter}"Anuwat"{tuple_delimiter}"expert"{tuple_delimiter}"Anuwat is a durian farmer recognized for his innovative farming techniques."){record_delimiter}
("entity"{tuple_delimiter}"Monthong"{tuple_delimiter}"durian_variety"{tuple_delimiter}"Monthong is a popular durian variety cultivated in Thailand."){record_delimiter}
("entity"{tuple_delimiter}"pruning technique"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Pruning technique refers to the method of trimming durian trees to optimize growth and yield."){record_delimiter}
("entity"{tuple_delimiter}"organic fertilizers"{tuple_delimiter}"farming_practice"{tuple_delimiter}"Organic fertilizers are natural substances used to enrich soil and promote plant health."){record_delimiter}
("entity"{tuple_delimiter}"Kasetsart University"{tuple_delimiter}"organization"{tuple_delimiter}"Kasetsart University is an educational institution conducting research on durian farming and diseases."){record_delimiter}
("entity"{tuple_delimiter}"durian root rot"{tuple_delimiter}"disease"{tuple_delimiter}"Durian root rot is a disease that affects the roots of durian trees, leading to reduced yields."){record_delimiter}
("entity"{tuple_delimiter}"Thai Durian Growers Association"{tuple_delimiter}"organization"{tuple_delimiter}"The Thai Durian Growers Association supports durian farmers and promotes best practices in the industry."){record_delimiter}
("relationship"{tuple_delimiter}"Anuwat"{tuple_delimiter}"Rayong"{tuple_delimiter}"Anuwat practices durian farming in Rayong province."{tuple_delimiter}"regional agriculture, farmer location"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Anuwat"{tuple_delimiter}"pruning technique"{tuple_delimiter}"Anuwat developed an innovative pruning technique for durian trees."{tuple_delimiter}"innovation, farming method"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"pruning technique"{tuple_delimiter}"Monthong"{tuple_delimiter}"The pruning technique is applied to Monthong durian trees to increase yield."{tuple_delimiter}"variety-specific practice, yield improvement"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Anuwat"{tuple_delimiter}"organic fertilizers"{tuple_delimiter}"Anuwat uses organic fertilizers in conjunction with his pruning technique."{tuple_delimiter}"integrated farming, input usage"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Kasetsart University"{tuple_delimiter}"Anuwat"{tuple_delimiter}"Researchers from Kasetsart University study Anuwat's farming methods."{tuple_delimiter}"research collaboration, knowledge transfer"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Kasetsart University"{tuple_delimiter}"durian root rot"{tuple_delimiter}"Kasetsart University conducts research on durian root rot to find solutions."{tuple_delimiter}"disease research, academic investigation"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Thai Durian Growers Association"{tuple_delimiter}"Anuwat"{tuple_delimiter}"The Thai Durian Growers Association recognizes and promotes Anuwat's farming techniques."{tuple_delimiter}"industry recognition, best practice promotion"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"durian farming, innovative techniques, disease research, yield improvement, industry support"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS["entity_continue_extraction"] = """
MANY entities and relationships were missed in the last extraction.

---Remember Steps---

1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

---Output---

Add them below using the same format:\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Goal---'

It appears some entities may have still been missed.

---Output---

Answer ONLY by `YES` OR `NO` if there are still entities that need to be added.
""".strip()

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user query about Knowledge Graph and Document Chunks provided in JSON format below.


---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Knowledge Base, and incorporating general knowledge relevant to the Knowledge Base. Do not include information not provided by Knowledge Base.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Knowledge Graph and Document Chunks---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating whether each source is from Knowledge Graph (KG) or Document Chunks (DC), and include the file path if available, in the following format: [KG/DC] file_path
- If you don't know the answer, just say so.
- Do not make anything up. Do not include information not provided by the Knowledge Base.
- Addtional user prompt: {user_prompt}

Response:"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Output the keywords in JSON format, it will be parsed by a JSON parser, do not add any extra content in output
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided provided in JSON format below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks(DC)---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating each source from Document Chunks(DC), and include the file path if available, in the following format: [DC] file_path
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks.
- Addtional user prompt: {user_prompt}

Response:"""

# TODO: deprecated
PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""
