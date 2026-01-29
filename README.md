# 📄 Fake Document Detection System

This project is a Streamlit-based document verification application that performs single-document visual forensic analysis to assist in identifying possible document tampering. The system accepts image and PDF documents, analyzes visual inconsistencies using OpenCV-based techniques, and highlights suspicious regions. It does not rely on machine learning models or reference documents and is designed to reduce false positives.

**Tools Used:** Python, Streamlit, OpenCV, NumPy, Pillow, PyMuPDF

**How It Works:**  
The user uploads a document, which is converted into an image and processed using computer vision techniques such as edge detection and contour analysis. Based on the strength and number of detected visual anomalies, the document is classified as REAL, SUSPICIOUS, or FAKE.

**How to Run:**  
1. Install dependencies using `pip install -r requirements.txt`  
2. Run the application using `streamlit run app.py`

**Disclaimer:**  
This system performs visual forensic analysis only and should be used as an assistance tool, not as a legal or official verification system.

**License:** MIT License

**Author:** K.sai sindhu (B.Tech Student)
