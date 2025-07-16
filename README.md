# AgriRAG: Agricultural RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system specifically designed for agricultural applications, combining the power of LightRAG and RAGAnything frameworks.

## 🚀 Overview

AgriRAG is an integrated system that leverages two powerful RAG frameworks:

- **LightRAG**: A lightweight, efficient RAG implementation with graph-based knowledge storage
- **RAGAnything**: A multimodal RAG framework that can process various types of content (text, images, documents, etc.)

## ⚠️ Current Status

**Current Release (v1.0.0)**: 
- ✅ **Supported**: `run_example.py` - Basic example script for testing and demonstration
- 🚧 **Coming Soon**: API server and Docker Compose support (planned for next release)

## 📁 Project Structure

```
AgriRAG/
├── src/
│   ├── LightRAG/              # Lightweight RAG component
│   │   ├── lightrag/          # Core LightRAG package
│   │   ├── lightrag_webui/    # Web UI for LightRAG
│   │   ├── tests/             # Test files
│   │   └── config.ini.example # LightRAG configuration example
│   └── RAGAnything/           # Multimodal RAG component
│       └── raganything/       # Core RAGAnything package
├── output/                    # Output directory for processed data
├── rag_storage/              # RAG storage directory
├── run_example.py            # Example usage script (Currently Supported)
├── pyproject.toml            # Project dependencies and configuration
├── uv.lock                   # Locked dependency versions
├── env.example               # Environment configuration example
├── Dockerfile                # Docker configuration (Coming Soon)
├── docker-compose.yml        # Docker Compose setup (Coming Soon)
└── README.md                 # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (fast Python package/dependency manager)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AgriRAG
   ```

2. **Install dependencies with uv:**
   ```bash
   uv pip install -r pyproject.toml
   # or, to install with dev dependencies:
   uv pip install -r pyproject.toml --extra dev
   ```

3. **Environment Configuration:**
   ```bash
   # Copy environment example
   cp env.example .env
   
   # Edit the .env file with your configuration
   ```

## 🚀 Quick Start

### Running the Example (Currently Supported)

```bash
# Run the unified example script
python run_example.py
```

This will:
- Initialize both LightRAG and RAGAnything
- Process agricultural documents
- Demonstrate querying capabilities
- Show multimodal processing

## 🔧 Configuration

### Environment Variables

```bash
# LLM Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Vector Database Configuration
VECTOR_DB_TYPE=postgres  # or milvus, qdrant, etc.
```

## 📊 Features

### LightRAG Features
- **Efficient Vector Storage**: Multiple vector database backends (PostgreSQL, Milvus, Qdrant)
- **Graph-based Knowledge**: Neo4j integration for entity-relationship graphs
- **Lightweight Design**: Optimized for performance and resource efficiency
- **Web UI**: User-friendly interface for document management and querying

### RAGAnything Features
- **Multimodal Processing**: Handle text, images, documents, and more
- **Flexible Content Types**: Support for various agricultural data formats
- **Batch Processing**: Efficient handling of large datasets
- **Custom Processors**: Extensible architecture for custom content types


## 🚧 Coming Soon (Next Release)

### API Server Features
- **RESTful API**: Complete HTTP API for all operations
- **Multimodal Support**: Handle both text and multimodal queries
- **Health Monitoring**: Built-in health checks and monitoring

### Docker Support
- **Containerized Deployment**: Complete Docker setup
- **Production Ready**: Nginx reverse proxy and proper service orchestration
- **Database Services**: PostgreSQL, Neo4j, and Redis containers




