# NLP Keyword Extraction Project

A Persian/Farsi text analysis tool that extracts keywords and keyphrases from text documents using the TextRank algorithm with POS tagging and natural language processing techniques.

## 🎯 Project Overview

This project implements an advanced keyword extraction system specifically designed for Persian/Farsi text processing. It uses the TextRank algorithm combined with Part-of-Speech (POS) tagging to identify the most important words and phrases in text documents.

## ✨ Features

- **Persian/Farsi Text Processing**: Optimized for Persian language with proper text normalization
- **Keyword Extraction**: Extracts individual keywords with their importance scores
- **Keyphrase Extraction**: Identifies meaningful multi-word phrases
- **POS Tagging**: Uses Hazm library for accurate Persian POS tagging
- **TextRank Algorithm**: Implements the TextRank algorithm for ranking words and phrases
- **Stop Word Filtering**: Comprehensive Persian stop word list for better results
- **Batch Processing**: Processes multiple text files automatically
- **Configurable Parameters**: Adjustable window size, damping coefficient, and convergence threshold

## 🏗️ Project Structure

```
nlp-keyword-extraction/
├── Input/                          # Input text files
│   ├── wiki_fa_1_NeuralNetwork.txt
│   ├── wiki_fa_2_DataBase.txt
│   └── wiki_fa_3_NLP.txt
├── Output/                         # Generated keyword and phrase files
│   ├── WordOut_*.txt              # Individual keywords with scores
│   └── PhraseOut_*.txt            # Keyphrases with scores
├── resources/                      # NLP models and libraries
│   ├── postagger.model            # POS tagging model
│   ├── chunker.model              # Chunking model
│   ├── langModel.mco              # Language model
│   ├── malt.jar                   # MaltParser
│   └── lib/                       # Java libraries
├── source.py                      # Main application code
├── Stop_words.txt                 # Persian stop words list
└── README.md                      # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- Java Runtime Environment (JRE) for MaltParser

### Dependencies

Install the required Python packages:

```bash
pip install hazm numpy
```

### Setup

1. Clone or download this repository
2. Ensure all resource files are in the `resources/` directory
3. Make sure Java is installed and accessible from command line

## 📖 Usage

### Basic Usage

1. Place your Persian text files in the `Input/` directory
2. Run the main script:

```bash
python source.py
```

3. Check the `Output/` directory for results:
   - `WordOut_[filename].txt`: Contains individual keywords with scores
   - `PhraseOut_[filename].txt`: Contains keyphrases with scores

### Output Format

**Keywords Output:**
```
عصبی - 2.9834683173198893
نورون ها - 2.4284856373486843
نورون - 2.3584436738484387
...
```

**Keyphrases Output:**
```
 نورون ها تشکیل - 2.3479472902508887
 شبکهٔ عصبی - 2.2743010535260852
 نورون های لایه های - 1.949765382008226
...
```

## 🔧 Configuration

The TextRank algorithm parameters can be adjusted in the `TextRank4Keyword` class:

- `d`: Damping coefficient (default: 0.85)
- `min_diff`: Convergence threshold (default: 1e-5)
- `steps`: Maximum iteration steps (default: 10)
- Window size for token pairs (default: 4)

## 🧠 Algorithm Details

### TextRank Implementation

The project implements the TextRank algorithm with the following steps:

1. **Text Preprocessing**: Normalization and sentence tokenization
2. **POS Tagging**: Using Hazm library for Persian POS tagging
3. **Candidate Selection**: Filtering words based on POS tags (N, V, Ne, AJ, AJe)
4. **Graph Construction**: Building co-occurrence graph with configurable window size
5. **Ranking**: Applying PageRank algorithm to rank words and phrases
6. **Scoring**: Calculating importance scores for keywords and keyphrases

### Supported POS Tags

- `N`: Nouns
- `V`: Verbs  
- `Ne`: Proper nouns
- `AJ`: Adjectives
- `AJe`: Comparative adjectives

## 📊 Example Results

For a text about neural networks, the system extracts:

**Top Keywords:**
- عصبی (Neural) - 2.98
- نورون ها (Neurons) - 2.43
- نورون (Neuron) - 2.36

**Top Keyphrases:**
- نورون ها تشکیل (Neurons formation) - 2.35
- شبکهٔ عصبی (Neural network) - 2.27
- نورون های لایه های (Neurons of layers) - 1.95

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- Performance improvements
- Additional language support
- New features

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Hazm](https://github.com/sobhe/hazm) - Persian NLP library
- [TextRank](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf) - Original algorithm paper
- MaltParser - For dependency parsing capabilities

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the existing issues in the repository
2. Create a new issue with detailed description
3. Include sample input and expected output

---

**Note**: This project is specifically optimized for Persian/Farsi text processing and may require adjustments for other languages.
