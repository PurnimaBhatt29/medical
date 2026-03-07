# Evaluation Metrics Guide

## Understanding the Evaluation Tab

The Evaluation tab in the Medical AI Assistant provides comprehensive metrics to assess the quality of AI-generated responses. Here's what each metric means:

## Core Metrics (Always Computed)

### 1. Faithfulness Score (0-1)
- **What it measures**: How well the response is grounded in the retrieved medical knowledge
- **How it works**: Compares the semantic similarity between the response and retrieved contexts using embeddings
- **Good score**: > 0.7 (70%)
- **Interpretation**:
  - High score (>0.7): Response is well-supported by retrieved documents
  - Low score (<0.5): Response may contain information not found in the knowledge base

### 2. Relevance Score (0-1)
- **What it measures**: How relevant the response is to the user's query
- **How it works**: Compares semantic similarity between the query and response
- **Good score**: > 0.7 (70%)
- **Interpretation**:
  - High score: Response directly addresses the question
  - Low score: Response may be off-topic or tangential

### 3. Context Precision (0-1)
- **What it measures**: Quality of the retrieved contexts - how relevant they are to the query
- **How it works**: Measures average similarity between query and all retrieved contexts
- **Good score**: > 0.6 (60%)
- **Interpretation**:
  - High score: Retrieved documents are highly relevant to the query
  - Low score: Retrieval system may have pulled irrelevant documents

### 4. Hallucination Risk (0-1)
- **What it measures**: Risk that the response contains fabricated information
- **How it works**: Inverse of faithfulness, adjusted for uncertainty markers
- **Good score**: < 0.3 (30%)
- **Interpretation**:
  - Low score: Response is well-grounded, low risk of hallucination
  - High score (>0.5): Higher risk of fabricated information - verify with healthcare provider

### 5. Overall Confidence (0-100%)
- **What it measures**: Overall quality and reliability of the response
- **How it works**: Weighted combination of all metrics:
  - Faithfulness: 35%
  - Relevance: 25%
  - Context Precision: 25%
  - (1 - Hallucination Risk): 15%
- **Quality Grades**:
  - Excellent: ≥85%
  - Good: 70-84%
  - Fair: 55-69%
  - Poor: <55%

## Retrieval Metrics (Optional - Require Ground Truth)

These metrics are **always 0 by default** unless you provide ground-truth relevant contexts.

### 6. Precision (0-1)
- **What it measures**: Proportion of retrieved contexts that are actually relevant
- **Formula**: (# retrieved that are relevant) / (# retrieved)
- **When to use**: When you know which contexts should be retrieved
- **How to enable**: Copy relevant text snippets from the retrieved contexts and paste them in the "Ground-truth relevant contexts" field

### 7. Recall (0-1)
- **What it measures**: Proportion of relevant contexts that were successfully retrieved
- **Formula**: (# retrieved that are relevant) / (# total relevant)
- **When to use**: When you have a complete list of relevant contexts
- **How to enable**: Provide all relevant context snippets in the ground-truth field

### 8. MRR (Mean Reciprocal Rank)
- **What it measures**: How early the first relevant document appears in results
- **Formula**: 1 / (rank of first relevant document)
- **Range**: 0-1 (1 = first result is relevant, 0 = no relevant results)
- **When to use**: To evaluate ranking quality

## How to Use the Evaluation Tab

### Basic Usage (No Ground Truth)
1. Enter your medical query
2. Click "Generate & Evaluate Response"
3. Review the 5 core metrics (Faithfulness, Relevance, Context Precision, Hallucination Risk, Confidence)
4. Check the Debug Info expander to see what was retrieved
5. Review retrieved contexts in the "Retrieved Contexts" expander

### Advanced Usage (With Ground Truth)
1. Enter your medical query
2. Run the evaluation once to see what contexts are retrieved
3. Open the "Retrieved Contexts" expander
4. Copy the text snippets that you consider relevant to the query
5. Paste them in the "Ground-truth relevant contexts" field (one per line)
6. Re-run the evaluation
7. Now Precision, Recall, and MRR will show non-zero values

## Why Are Precision, Recall, and MRR Showing 0?

**This is expected behavior!** These metrics require you to manually specify which contexts are relevant (ground truth). Without ground truth, they default to 0.

To compute these metrics:
1. Look at the retrieved contexts in the expander
2. Identify which ones are actually relevant to your query
3. Copy those relevant snippets
4. Paste them in the "Ground-truth relevant contexts" field
5. Re-run the evaluation

## Example Workflow

**Query**: "What are the side effects of aspirin?"

**Step 1**: Run evaluation
- Faithfulness: 0.63 (63%)
- Relevance: 0.70 (70%)
- Context Precision: 0.42 (42%)
- Hallucination Risk: 0.29 (29%)
- Confidence: 60.6% (Fair)
- Precision/Recall/MRR: 0 (no ground truth provided)

**Step 2**: Review retrieved contexts and identify relevant ones
- Context 1: About aspirin contraindications ✓ (relevant)
- Context 2: About naproxen side effects ✗ (not relevant)
- Context 3: About aspirin dosage ✓ (relevant)

**Step 3**: Copy relevant context text and paste in ground-truth field

**Step 4**: Re-run evaluation
- Now Precision: 0.40 (2 out of 5 retrieved were relevant)
- Recall: 1.0 (both relevant contexts were retrieved)
- MRR: 1.0 (first result was relevant)

## Tips for Interpretation

1. **Medical Safety**: Always verify AI responses with healthcare providers, especially if:
   - Hallucination Risk > 0.5
   - Faithfulness < 0.5
   - Confidence < 55%

2. **Context Quality**: If Context Precision is low (<0.4), the retrieval system may need improvement or the knowledge base may lack relevant information

3. **Response Quality**: High Relevance + High Faithfulness = Trustworthy response

4. **Debugging**: Use the Debug Info and Retrieved Contexts expanders to understand what the system is working with

## Technical Details

- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Similarity Metric**: Cosine similarity
- **Retrieval Strategy**: HyDE (Hypothetical Document Embeddings) with cross-encoder reranking
- **Cross-Encoder**: cross-encoder/ms-marco-MiniLM-L-6-v2
