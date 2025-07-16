# RAGAnything: Multimodal RAG Framework

A comprehensive multimodal Retrieval-Augmented Generation (RAG) framework that can process various types of content including text, images, tables, and equations.

## 🚀 Features

- **Multimodal Processing**: Handle text, images, tables, equations, and documents
- **Universal Document Support**: PDFs, Office documents (DOC/DOCX/PPT/PPTX/XLS/XLSX), images
- **Specialized Content Analysis**: Dedicated processors for different content types
- **Multimodal Knowledge Graph**: Automatic entity extraction and cross-modal relationships
- **Hybrid Retrieval**: Advanced search across textual and multimodal content
- **LightRAG Integration**: Built on top of LightRAG for enhanced capabilities

## 📦 Installation

```bash
# Install from source (recommended)
cd RAGAnything
pip install -e .

# Or install from PyPI
pip install raganything
```

## 🚀 Quick Start

### Basic Usage
```python
import asyncio
from RAGAnything.raganything import RAGAnything
from LightRAG.lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from LightRAG.lightrag.utils import EmbeddingFunc

async def main():
    # Initialize RAGAnything
    rag = RAGAnything(
        llm_model_func=gpt_4o_mini_complete,
        embedding_func=EmbeddingFunc(
            embedding_dim=1536,
            max_token_size=8192,
            func=openai_embed
        ),
        vision_model_func=gpt_4o_mini_complete  # For image processing
    )
    
    # Process a multimodal document
    await rag.process_document_complete(
        file_path="path/to/your/document.pdf",
        output_dir="./output"
    )
    
    # Query the processed content
    result = await rag.query_with_multimodal(
        "What information is shown in the tables and images?",
        mode="hybrid"
    )
    print(result.answer)

asyncio.run(main())
```

### Processing Different Content Types

```python
# Process text content
text_content = "Your text content here..."
await rag.process_text_content(text_content)

# Process image content
image_path = "path/to/image.jpg"
await rag.process_image_content(image_path)

# Process table content
table_data = [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]
await rag.process_table_content(table_data)

# Process mathematical equations
equation = "E = mc^2"
await rag.process_equation_content(equation)
```

## 🔧 Configuration

### Environment Variables
```bash
# LLM Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Vision Model Configuration
VISION_MODEL_API_KEY=your_vision_model_key

# Processing Configuration
MAX_CONCURRENT_PROCESSES=4
CHUNK_SIZE=1000
```

### Supported File Formats
- **Documents**: PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX
- **Images**: JPG, PNG, GIF, BMP, TIFF
- **Text**: TXT, MD, JSON, CSV
- **Other**: Any format supported by MinerU

## 📚 Documentation

- **Context Processing**: `docs/context_aware_processing.md`
- **API Reference**: Available in the source code
- **Examples**: Check the examples directory

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

- **Original Repository**: https://github.com/HKUDS/RAG-Anything
- **LightRAG**: https://github.com/HKUDS/LightRAG
- **Discord**: https://discord.gg/yF2MmDJyGJ
