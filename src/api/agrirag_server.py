#!/usr/bin/env python3
"""
AgriRAG Unified API Server
Provides RESTful API endpoints for both LightRAG and RAGAnything functionality.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add the parent directory to the path to import LightRAG and RAGAnything
sys.path.append(str(Path(__file__).parent.parent))

from LightRAG.lightrag import LightRAG, QueryParam
from LightRAG.lightrag.kg.shared_storage import initialize_pipeline_status
from LightRAG.lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from RAGAnything.raganything import RAGAnything

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for API requests/responses
class QueryRequest(BaseModel):
    query: str
    mode: str = "hybrid"
    chunk_top_k: int = 5
    conversation_history: Optional[List[Dict[str, str]]] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float


class DocumentUploadResponse(BaseModel):
    message: str
    document_id: str
    status: str


class HealthResponse(BaseModel):
    status: str
    lightrag_status: str
    raganything_status: str


# Initialize FastAPI app
app = FastAPI(
    title="AgriRAG API",
    description="Unified API for Agricultural RAG System combining LightRAG and RAGAnything",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgriRAGServer:
    """Main server class that manages LightRAG and RAGAnything instances."""

    def __init__(self):
        self.lightrag: Optional[LightRAG] = None
        self.raganything: Optional[RAGAnything] = None
        self.working_dir = "./rag_storage"
        self.initialized = False

    async def initialize(self):
        """Initialize both LightRAG and RAGAnything instances."""
        if self.initialized:
            return

        try:
            logger.info("Initializing AgriRAG server...")

            # Initialize LightRAG
            self.lightrag = LightRAG(
                working_dir=self.working_dir,
                embedding_func=openai_embed,
                llm_model_func=gpt_4o_mini_complete,
            )

            # Initialize storages and pipeline
            await self.lightrag.initialize_storages()
            await initialize_pipeline_status()

            # Initialize RAGAnything with the same LightRAG instance
            self.raganything = RAGAnything(
                lightrag=self.lightrag, vision_model_func=gpt_4o_mini_complete
            )

            self.initialized = True
            logger.info("AgriRAG server initialized successfully!")

        except Exception as e:
            logger.error(f"Failed to initialize AgriRAG server: {e}")
            raise


# Global server instance
agrirag_server = AgriRAGServer()


@app.on_event("startup")
async def startup_event():
    """Initialize the server on startup."""
    await agrirag_server.initialize()


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Welcome to AgriRAG API",
        "version": "1.0.0",
        "description": "Unified API for Agricultural RAG System",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if agrirag_server.initialized else "initializing",
        lightrag_status="ready" if agrirag_server.lightrag else "not_ready",
        raganything_status="ready" if agrirag_server.raganything else "not_ready",
    )


@app.post("/query", response_model=QueryResponse)
async def query_knowledge(request: QueryRequest):
    """Query the knowledge base using LightRAG."""
    if not agrirag_server.lightrag:
        raise HTTPException(status_code=503, detail="LightRAG not initialized")

    try:
        query_param = QueryParam(
            query=request.query,
            mode=request.mode,
            chunk_top_k=request.chunk_top_k,
            conversation_history=request.conversation_history or [],
        )

        result = await agrirag_server.lightrag.aquery(query_param)

        return QueryResponse(
            answer=result.answer if hasattr(result, "answer") else str(result),
            sources=result.sources if hasattr(result, "sources") else [],
            confidence=result.confidence if hasattr(result, "confidence") else 0.8,
        )

    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/documents/text", response_model=DocumentUploadResponse)
async def upload_text_document(text: str = Form(...)):
    """Upload text document to LightRAG."""
    if not agrirag_server.lightrag:
        raise HTTPException(status_code=503, detail="LightRAG not initialized")

    try:
        await agrirag_server.lightrag.ainsert(text)

        return DocumentUploadResponse(
            message="Text document uploaded successfully",
            document_id=f"text_{hash(text) % 1000000}",
            status="processed",
        )

    except Exception as e:
        logger.error(f"Error uploading text document: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/documents/multimodal", response_model=DocumentUploadResponse)
async def upload_multimodal_document(
    file: UploadFile = File(...), description: Optional[str] = Form(None)
):
    """Upload multimodal document using RAGAnything."""
    if not agrirag_server.raganything:
        raise HTTPException(status_code=503, detail="RAGAnything not initialized")

    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Process with RAGAnything
        await agrirag_server.raganything.process_document_complete(
            file_path=temp_path, output_dir="./output"
        )

        # Clean up temp file
        os.remove(temp_path)

        return DocumentUploadResponse(
            message="Multimodal document uploaded and processed successfully",
            document_id=f"multimodal_{hash(file.filename) % 1000000}",
            status="processed",
        )

    except Exception as e:
        logger.error(f"Error uploading multimodal document: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.delete("/documents")
async def clear_all_documents():
    """Clear all documents from the knowledge base."""
    if not agrirag_server.lightrag:
        raise HTTPException(status_code=503, detail="LightRAG not initialized")

    try:
        # Clear all storages
        await agrirag_server.lightrag.text_chunks.drop()
        await agrirag_server.lightrag.full_docs.drop()
        await agrirag_server.lightrag.entities_vdb.drop()
        await agrirag_server.lightrag.relationships_vdb.drop()
        await agrirag_server.lightrag.chunks_vdb.drop()
        await agrirag_server.lightrag.chunk_entity_relation_graph.drop()
        await agrirag_server.lightrag.doc_status.drop()

        return {"message": "All documents cleared successfully"}

    except Exception as e:
        logger.error(f"Error clearing documents: {e}")
        raise HTTPException(status_code=500, detail=f"Clear failed: {str(e)}")


@app.get("/documents")
async def list_documents():
    """List all documents in the knowledge base."""
    if not agrirag_server.lightrag:
        raise HTTPException(status_code=503, detail="LightRAG not initialized")

    try:
        # This would need to be implemented based on the actual storage backend
        # For now, return a placeholder
        return {
            "documents": [],
            "total_count": 0,
            "message": "Document listing not yet implemented",
        }

    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=f"List failed: {str(e)}")


@app.post("/query/multimodal", response_model=QueryResponse)
async def query_multimodal(request: QueryRequest):
    """Query multimodal content using RAGAnything."""
    if not agrirag_server.raganything:
        raise HTTPException(status_code=503, detail="RAGAnything not initialized")

    try:
        result = await agrirag_server.raganything.query_with_multimodal(
            query=request.query, mode=request.mode
        )

        return QueryResponse(
            answer=result.answer if hasattr(result, "answer") else str(result),
            sources=result.sources if hasattr(result, "sources") else [],
            confidence=result.confidence if hasattr(result, "confidence") else 0.8,
        )

    except Exception as e:
        logger.error(f"Error querying multimodal content: {e}")
        raise HTTPException(
            status_code=500, detail=f"Multimodal query failed: {str(e)}"
        )


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Run the server
    uvicorn.run(
        "agrirag_server:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
