# LightRAG: Lightweight RAG Framework

A lightweight and efficient Retrieval-Augmented Generation (RAG) framework with graph-based knowledge storage.

## 🚀 Features

- **Efficient Vector Storage**: Multiple vector database backends (PostgreSQL, Milvus, Qdrant, FAISS)
- **Graph-based Knowledge**: Neo4j integration for entity-relationship graphs
- **Lightweight Design**: Optimized for performance and resource efficiency
- **Web UI**: User-friendly interface for document management and querying
- **API Server**: RESTful API with Ollama-compatible interface
- **Multimodal Support**: Integration with RAGAnything for document processing

## 📦 Installation

### Core Installation
```bash
# Install from source (recommended)
cd LightRAG
pip install -e .

# Or install from PyPI
pip install lightrag-hku
```

### Server Installation (with Web UI)
```bash
# Install with API support
pip install "lightrag-hku[api]"

# Or from source
pip install -e ".[api]"
```

## 🚀 Quick Start

### Basic Usage
```python
import asyncio
from LightRAG.lightrag import LightRAG, QueryParam
from LightRAG.lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from LightRAG.lightrag.kg.shared_storage import initialize_pipeline_status

async def main():
    # Initialize LightRAG
    rag = LightRAG(
        working_dir="./rag_storage",
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
    )
    
    # IMPORTANT: Initialize storages and pipeline
    await rag.initialize_storages()
    await initialize_pipeline_status()
    
    # Insert documents
    await rag.ainsert("Your documents here...")
    
    # Query the system
    query_param = QueryParam(
        query="Your question here?",
        chunk_top_k=5
    )
    result = await rag.aquery(query_param)
    print(result.answer)

asyncio.run(main())
```

### Web UI
```bash
# Start the server
lightrag-server

# Access at http://localhost:8000
```

### Docker
```bash
# Using Docker Compose
cp env.example .env
docker compose up
```

## 🔧 Configuration

### Environment Variables
```bash
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=lightrag_db
POSTGRES_USER=lightrag_user
POSTGRES_PASSWORD=your_password

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# LLM Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### Supported Storage Backends
- **Vector Databases**: PostgreSQL, Milvus, Qdrant, FAISS, Redis
- **Graph Databases**: Neo4j, NetworkX, Memgraph
- **Document Storage**: JSON, MongoDB, TiDB

## 📚 Documentation

- **API Documentation**: `lightrag/api/README.md`
- **Algorithm Details**: `docs/Algorithm.md`
- **Docker Deployment**: `docs/DockerDeployment.md`

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **Original Repository**: https://github.com/HKUDS/LightRAG
- **Paper**: https://arxiv.org/abs/2410.05779
- **Discord**: https://discord.gg/yF2MmDJyGJ
