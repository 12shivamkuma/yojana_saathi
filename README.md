# 🇮🇳 Yojana Saathi – AI-Powered Government Scheme Assistant

**Your voice-based companion for discovering Indian government welfare schemes.**

Yojana Saathi is an AI-powered, Hindi voice assistant that helps people discover relevant Indian government welfare schemes through natural voice interactions. Users can describe their needs in Hindi, and the application identifies potentially relevant government schemes and provides information through both text and generated speech.

The project aims to make government scheme information more accessible, particularly for people who may find traditional websites and complex application processes difficult to navigate.

## 🎯 Problem Statement

India has numerous government welfare schemes covering agriculture, healthcare, housing, employment, education, and financial inclusion.

However, many citizens face challenges such as:
- Lack of awareness about available government schemes.
- Difficulty navigating government portals.
- Language barriers.
- Limited digital literacy.
- Difficulty identifying schemes relevant to their needs.

## 💡 Our Solution

Yojana Saathi provides a simple voice-based interface where users can explain their requirements in Hindi.

The system processes their speech, searches a knowledge base of government schemes, generates a relevant Hindi response, and converts that response into audio.

## ✨ Key Features

- 🎙️ **Hindi Voice Input:** Users can describe their needs through voice recording.
- 🧠 **AI-Powered Speech Recognition:** Uses Gnani AI Prisma for converting speech into text.
- 🔎 **Government Scheme Matching:** Identifies relevant schemes using a keyword-based retrieval system.
- 📚 **Knowledge Base:** Contains information about 10 Indian government schemes.
- 📝 **Informative Responses:** Displays scheme descriptions, benefits, eligibility conditions, and official website links.
- 🔊 **Hindi Text-to-Speech:** Uses Gnani AI Timbre to generate spoken responses.
- 🌐 **Interactive Web Application:** Built using Streamlit for a simple and accessible user experience.

## 🔄 How It Works

1. **Voice Input:** The user records a query in Hindi.
2. **Speech-to-Text:** Gnani AI Prisma converts the recorded audio into text.
3. **Scheme Retrieval:** The retrieval system searches the knowledge base for relevant schemes.
4. **Response Generation:** The application generates a response using the matched scheme information.
5. **Text-to-Speech:** Gnani AI Timbre converts the response into audio.
6. **Output:** The user receives both written and spoken information.

## 🏛️ Government Schemes Covered

The current knowledge base includes:

| No. | Government Scheme | Main Area |
|---|---|---|
| 1 | PM-KISAN Samman Nidhi | Agriculture |
| 2 | Ayushman Bharat PM-JAY | Healthcare |
| 3 | Pradhan Mantri Ujjwala Yojana | LPG Connection |
| 4 | Pradhan Mantri Jan Dhan Yojana | Financial Inclusion |
| 5 | MGNREGA | Rural Employment |
| 6 | PM Awas Yojana – Gramin | Rural Housing |
| 7 | PM Vishwakarma Yojana | Traditional Artisans |
| 8 | PM SVANidhi | Street Vendors |
| 9 | Prime Minister Employment Generation Programme (PMEGP) | Entrepreneurship |
| 10 | National Scholarship Portal Schemes | Education |

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Web application interface |
| Gnani AI Prisma | Speech-to-Text |
| Gnani AI Timbre | Text-to-Speech |
| JSON | Government scheme knowledge base |
| Requests | API communication |
| python-dotenv | Secure environment variable management |

## 📁 Project Structure

```text
Yojana-Saathi/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── utils/
│   ├── stt.py
│   ├── tts.py
│   ├── retriever.py
│   └── response.py
│
├── kb/
│   └── schemes.json
│
├── audio/
│
└── test files
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Yojana-Saathi.git
cd Yojana-Saathi
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root directory.

Add your Gnani AI API key:

```env
GNANI_API_KEY=your_gnani_api_key_here
```

**Important:** Never upload your actual `.env` file or API key to GitHub.

### 5. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🧪 Testing

The project includes separate test scripts for different components:

- `test_stt.py` – Tests speech recognition.
- `test_tts.py` – Tests speech generation.
- `test_retriever.py` – Tests scheme retrieval.
- `test_response.py` – Tests response generation.
- `test_full_pipeline.py` – Tests the complete processing pipeline.
- `test_10_schemes.py` – Tests matching across 10 scheme-related queries.

## 🔐 Responsible AI and Limitations

- The system provides preliminary information and does not determine a user's official eligibility.
- Scheme matching currently uses keyword-based retrieval and may not understand every variation of a user's query.
- Information in the knowledge base should be checked against official government sources.
- Users should verify eligibility, application procedures, and benefits through the respective official portals.
- The application does not require users to provide sensitive information such as Aadhaar numbers, bank account details, or passwords.

## 🚀 Future Improvements

- Support for additional Indian languages.
- Improved semantic search using NLP and embeddings.
- Integration with more government schemes.
- More robust handling of regional accents and speech variations.
- Retrieval from verified official government sources.
- Deployment on a cloud platform for wider accessibility.

## 🤝 Contribution

Contributions and suggestions are welcome!

You can contribute by improving scheme information, enhancing retrieval accuracy, adding language support, or improving the user interface.

## 📜 Disclaimer

Yojana Saathi is an informational project designed to improve awareness of government welfare schemes. It is not an official government application and is not affiliated with any government department.

Always consult the respective official government portals for the latest and authoritative information.

---

**Built with Python, Streamlit, and Gnani AI.**

*Making government scheme information more accessible, one conversation at a time.* 🇮🇳
