import asyncio
import os

from src.LightRAG.lightrag import LightRAG
from src.LightRAG.lightrag.llm.openai import openai_complete_if_cache, openai_embed
from src.LightRAG.lightrag.utils import EmbeddingFunc
from src.RAGAnything.raganything import RAGAnything, RAGAnythingConfig

WORKING_DIR = "./rag_storage"


async def main():
    # Create RAGAnything configuration
    config = RAGAnythingConfig(
        working_dir=WORKING_DIR,
        mineru_parse_method="auto",
        enable_image_processing=True,
        enable_table_processing=True,
        enable_equation_processing=True,
    )

    # Define LLM model function
    def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
        return openai_complete_if_cache(
            "gpt-4.1-nano",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=os.getenv("LLM_BINDING_API_KEY"),
            base_url=os.getenv("LLM_BINDING_HOST"),
            **kwargs,
        )

    # Define vision model function for image processing
    def vision_model_func(
        prompt, system_prompt=None, history_messages=[], image_data=None, **kwargs
    ):
        if image_data:
            return openai_complete_if_cache(
                "gpt-4o",
                "",
                system_prompt=None,
                history_messages=[],
                messages=[
                    {"role": "system", "content": system_prompt}
                    if system_prompt
                    else None,
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                },
                            },
                        ],
                    }
                    if image_data
                    else {"role": "user", "content": prompt},
                ],
                api_key=os.getenv("LLM_BINDING_API_KEY"),
                base_url=os.getenv("LLM_BINDING_HOST"),
                **kwargs,
            )
        else:
            return llm_model_func(prompt, system_prompt, history_messages, **kwargs)

    # Define embedding function
    embedding_func = EmbeddingFunc(
        embedding_dim=1536,
        max_token_size=8192,
        func=lambda texts: openai_embed(
            texts,
            model="text-embedding-3-large",
            api_key=os.getenv("EMBEDDING_BINDING_API_KEY"),
            base_url=os.getenv("EMBEDDING_BINDING_HOST"),
        ),
    )

    light_rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=embedding_func,
        llm_model_func=llm_model_func,
        llm_model_name="gpt-4.1-nano",
        kv_storage="PGKVStorage",
        vector_storage="PGVectorStorage",
        graph_storage="Neo4JStorage",
        doc_status_storage="PGDocStatusStorage",
    )

    # Initialize RAGAnything
    rag = RAGAnything(
        lightrag=light_rag,
        config=config,
        vision_model_func=vision_model_func,
    )

    # Process a document
    await rag.process_document_complete(
        file_path="/Users/mac/thinhquyen/vns/code/argi_kb/data/doc-data/pdf/1640919293Durian Production Guide.pdf",
        output_dir="./output",
        parse_method="auto",
    )

    # Query the processed content
    # Pure text query - for basic knowledge base search
    text_result = await rag.aquery("How tall is the durian tree?", mode="hybrid")
    print("Text query result:", text_result)

    # # Multimodal query with specific multimodal content
    # multimodal_result = await rag.aquery_with_multimodal(
    #     "Explain this formula and its relevance to the document content",
    #     multimodal_content=[
    #         {
    #             "type": "equation",
    #             "latex": "P(d|q) = \\frac{P(q|d) \\cdot P(d)}{P(q)}",
    #             "equation_caption": "Document relevance probability",
    #         }
    #     ],
    #     mode="hybrid",
    # )
    # print("Multimodal query result:", multimodal_result)


if __name__ == "__main__":
    asyncio.run(main())
