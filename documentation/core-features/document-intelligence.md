# Document Intelligence - TAF-3000

OPSIIE's File Manager TAF-3000 provides intelligent document processing with natural language querying.

## 📁 Overview

- **Formats**: PDF, CSV, DOCX, TXT, XLSX
- **Analysis**: Intelligent parsing and extraction
- **Queries**: Ask questions about content
- **Context**: Maintains file context
- **AI**: Uses Ollama/Llama3 for responses

## 📖 Commands

### /read - Load File
```bash
/read "<file_path>"
```

**Examples:**
```bash
/read "C:\Documents\report.pdf"
/read "E:\Data\sales.csv"
/read "C:\Notes\meeting.docx"
```

### Ask Questions
After loading, ask naturally:
```
What are the main conclusions?
Which product had highest sales?
Summarize the methodology
```

### /open - Reopen Last File
```bash
/open
```

### /close - Close Context
```bash
/close
```

## 📊 Supported Formats

- **PDF**: PyPDF2, pdfplumber
- **CSV**: pandas
- **DOCX**: python-docx
- **TXT**: built-in
- **XLSX**: pandas

## 💡 Best Practices

**Use full paths:**
```bash
✅ /read "C:\Users\Name\file.pdf"
❌ /read "file.pdf"
```

**Be specific in queries:**
```
✅ "What does section 3 say about revenue?"
❌ "Tell me about it"
```

## 🚨 Troubleshooting

**File not found:** Check path, use absolute paths
**Unsupported format:** Only PDF, CSV, DOCX, TXT, XLSX
**Query fails:** Rephrase, be more specific

---

**TAF-3000 makes documents intelligible.** 📁