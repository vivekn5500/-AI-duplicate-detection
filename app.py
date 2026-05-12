import streamlit as st
import pandas as pd
import re
import fitz
from deep_translator import GoogleTranslator
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import yake
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

st.set_page_config(page_title="Ultimate AI Duplicate Detector", layout="wide")

# ---------- TITLE ----------
st.title("🚀 Ultimate AI Duplicate Detection System")
st.write("Multilingual | BERT | Keywords | Graph | CSV/PDF Support")

# ---------- CLEAN ----------
def clean_text(text):
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------- SAFE TRANSLATION ----------
def safe_translate(text):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)

        if translated is None or not isinstance(translated, str):
            return text
        if not translated.strip():
            return text

        return translated
    except:
        return text

# ---------- KEYWORDS ----------
def extract_keywords(text):
    kw_extractor = yake.KeywordExtractor(lan="en", top=3)
    keywords = kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

# ---------- GRAPH (FIXED) ----------
def create_graph(data, similarity_matrix, threshold):
    G = nx.Graph()

    for i, text in enumerate(data):
        G.add_node(i, label=str(text))

    for i in range(len(data)):
        for j in range(i+1, len(data)):
            score = float(similarity_matrix[i][j])
            if score > threshold:
                G.add_edge(i, j, weight=float(round(score, 2)))

    net = Network(height="500px", width="100%")
    net.from_nx(G)
    net.save_graph("graph.html")

    return "graph.html"

# ---------- INPUT ----------
st.subheader("📂 Input Options")
option = st.radio("Choose Input Type", ["Manual Input", "CSV Upload", "PDF Upload"])

data = []

# ---------- MANUAL ----------
if option == "Manual Input":
    user_input = st.text_area("📥 Enter Records (one per line)", height=200)
    if user_input:
        data = [d for d in user_input.split("\n") if d.strip()]

# ---------- CSV ----------
elif option == "CSV Upload":
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        data = df.iloc[:, 0].dropna().tolist()
        st.success("CSV Loaded Successfully")

# ---------- PDF ----------
elif option == "PDF Upload":
    file = st.file_uploader("Upload PDF", type=["pdf"])
    if file:
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        text_data = []

        for page in pdf:
            text_data.extend(page.get_text().split("\n"))

        data = [t for t in text_data if t.strip()]
        st.success("PDF Loaded Successfully")

# ---------- SETTINGS ----------
threshold = st.slider("🎚️ Similarity Threshold", 0.0, 1.0, 0.8)

# ---------- RUN ----------
if st.button("⚡ Run AI Detection"):

    if not data:
        st.warning("⚠️ Please provide input data")
    else:
        cleaned_data = []
        original_data = []

        st.subheader("🔄 Processing Pipeline")

        for item in data:
            translated = safe_translate(item)
            cleaned = clean_text(translated)

            if len(cleaned) > 2:
                cleaned_data.append(cleaned)
                original_data.append(item)

        # Remove duplicates safely
        unique_pairs = list(dict.fromkeys(zip(original_data, cleaned_data)))
        original_data, cleaned_data = zip(*unique_pairs)
        original_data = list(original_data)
        cleaned_data = list(cleaned_data)

        # ---------- BERT ----------
        st.subheader("🧠 BERT Semantic Processing")
        embeddings = model.encode(cleaned_data)
        similarity_matrix = cosine_similarity(embeddings)

        # ---------- GROUPING ----------
        visited = set()
        groups = []

        for i in range(len(cleaned_data)):
            if i in visited:
                continue

            group = [i]
            for j in range(i+1, len(cleaned_data)):
                if similarity_matrix[i][j] > threshold:
                    group.append(j)
                    visited.add(j)

            if len(group) > 1:
                groups.append(group)

        # ---------- GROUP OUTPUT ----------
        st.subheader("🔗 Duplicate Groups")

        if not groups:
            st.info("No duplicates found")
        else:
            for idx, group in enumerate(groups):
                st.markdown(f"### Group {idx+1}")
                for i in group:
                    st.write(f"• {original_data[i]}")

        # ---------- KEYWORDS ----------
        st.subheader("🔍 Keyword Extraction")
        for i, text in enumerate(cleaned_data):
            keywords = extract_keywords(text)
            st.write(f"{original_data[i]} → {', '.join(keywords)}")

        # ---------- DETAILED ----------
        st.subheader("📊 Detailed Matches")

        total_matches = 0

        for i in range(len(cleaned_data)):
            for j in range(i+1, len(cleaned_data)):
                score = similarity_matrix[i][j]

                if score > threshold:
                    total_matches += 1

                    if score > 0.9:
                        level = "🟢 High"
                    elif score > 0.8:
                        level = "🟡 Medium"
                    else:
                        level = "🔴 Low"

                    words1 = set(cleaned_data[i].split())
                    words2 = set(cleaned_data[j].split())
                    common = words1.intersection(words2)

                    st.write(f"{original_data[i]} ↔ {original_data[j]}")
                    st.write(f"Score: {score:.2f} | {level}")
                    st.write(f"Matched Words: {', '.join(common)}")
                    st.write("---")

        # ---------- INSIGHTS ----------
        st.subheader("📈 Insights Dashboard")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Records", len(original_data))

        with c2:
            st.metric("Matches", total_matches)

        with c3:
            st.metric("Groups", len(groups))

        # ---------- GRAPH ----------
        st.subheader("🌐 Graph Visualization")

        graph_file = create_graph(original_data, similarity_matrix, threshold)
        components.html(open(graph_file).read(), height=500)

        # ---------- MATRIX ----------
        with st.expander("🔍 Similarity Matrix"):
            labels = [f"{original_data[i]} ({i})" for i in range(len(original_data))]
            df = pd.DataFrame(similarity_matrix, columns=labels, index=labels)
            st.dataframe(df)

        st.success("🎉 System Completed Successfully!")