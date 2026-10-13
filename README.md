# 🌐 DupDetector AI

**Multilingual AI-Based Duplicate Detection System**

DupDetector AI is a Python-based application that identifies semantically similar text records across multiple languages using NLP, Sentence-BERT embeddings, and cosine similarity.

It provides an interactive dashboard to analyze text, identify potential duplicates, and visualize relationships between records.

## ✨ Features

- 🌍 **Multilingual Analysis** — Analyze text in multiple languages.
- 📂 **Multiple Input Sources** — Manual text, CSV files, and PDF documents.
- 🧠 **AI-Powered Matching** — Generate semantic embeddings using Sentence-BERT.
- 🎯 **Similarity Threshold** — Configure the cutoff for matching records.
- 📊 **Duplicate Clusters** — Group potentially similar records.
- 🌐 **Similarity Network Graph** — Visualize relationships between records.
- 🔍 **Match Diagnostics** — Inspect matched pairs and similarity scores.
- 📈 **Cosine Similarity Matrix** — Explore pairwise similarity scores.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive dashboard |
| Sentence Transformers | Semantic embeddings |
| `all-MiniLM-L6-v2` | Pre-trained AI model |
| Scikit-learn | Cosine similarity |
| Pandas | Data processing |
| Deep Translator | Translation support |
| PyMuPDF | PDF text extraction |
| NetworkX & PyVis | Network visualization |
| YAKE | Keyword extraction |

## ⚙️ How It Works

1. Input text manually or upload a CSV/PDF file.
2. Extract and preprocess text records.
3. Apply the multilingual translation workflow where required.
4. Generate semantic embeddings using Sentence-BERT.
5. Calculate cosine similarity between records.
6. Apply the configured threshold and identify potential matches.
7. Display clusters, matched pairs, network graphs, and similarity scores.

## 🚀 Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/vivekn5500/-AI-duplicate-detection.git
cd -AI-duplicate-detection
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start the application**

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 🏢 Potential Applications

- **Banking:** Identify potentially duplicate customer records.
- **Government:** Detect repeated citizen complaints.
- **Healthcare:** Flag potentially duplicate patient records for review.
- **Education:** Find similar assignments and academic submissions.
- **Research:** Identify similar research descriptions and topics.
- **E-commerce:** Analyze similar customer reviews and feedback.

## 🔮 Future Scope

- Database integration for persistent storage.
- REST API backend and improved frontend architecture.
- Scalable vector search for large datasets.
- Downloadable analysis reports.
- Authentication and cloud deployment.

## 👨‍💻 Author

**Vivek Neharkar**

GitHub: [@vivekn5500](https://github.com/vivekn5500)

*An MCA academic project exploring multilingual semantic text analysis and AI-based duplicate detection.*
