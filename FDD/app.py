import streamlit as st
import cv2
import numpy as np
from PIL import Image
import fitz

# ---------------- CONFIG ---------------- #
st.set_page_config("Document Verification", layout="wide")
st.title("📄 Document Verification System")
st.caption("Conservative forensic analysis (Low false positives)")

# ---------------- LOAD FILE ---------------- #
def load_file(uploaded_file):
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext in ["jpg", "jpeg", "png"]:
        return np.array(Image.open(uploaded_file).convert("RGB"))
    elif ext == "pdf":
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = pdf[0]
        pix = page.get_pixmap(dpi=200)
        return np.array(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    return None

# ---------------- DETECT ---------------- #
def detect_visual_tampering(image):
    image = cv2.resize(image, (600, 800))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blur, 150, 300)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=1)

    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    marked = image.copy()
    red_boxes = 0

    for c in contours:
        area = cv2.contourArea(c)
        if area < 1200 or area > 6000:
            continue

        x, y, w, h = cv2.boundingRect(c)

        if w > 4 * h:  # ignore text lines
            continue

        # Strong anomaly only
        cv2.rectangle(marked, (x, y), (x + w, y + h), (0, 0, 255), 3)
        red_boxes += 1

    return marked, red_boxes, image

# ---------------- DECISION ---------------- #
def verdict(red_boxes):
    if red_boxes >= 3:
        return "FAKE", 60
    elif red_boxes >= 1:
        return "SUSPICIOUS", 80
    else:
        return "REAL", 95

# ---------------- UI ---------------- #
file = st.file_uploader("Upload document", ["jpg", "jpeg", "png", "pdf"])

if file:
    image = load_file(file)
    marked, red_count, resized = detect_visual_tampering(image)
    result, confidence = verdict(red_count)

    col1, col2 = st.columns(2)
    with col1:
        st.image(resized, "Uploaded Document", use_container_width=True)
    with col2:
        st.image(marked, "Detected Tampering", use_container_width=True)

    st.markdown("## 📊 Result")
    st.write(f"🔴 Strong anomalies detected: **{red_count}**")
    st.write(f"🎯 Confidence: **{confidence}%**")

    if result == "REAL":
        st.success("🟢 REAL — No strong tampering detected")
    elif result == "SUSPICIOUS":
        st.warning("🟡 SUSPICIOUS — Minor irregularities found")
    else:
        st.error("🔴 FAKE — Clear visual manipulation detected")
