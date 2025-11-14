# Vietnamese Sentiment Assistant

Ứng dụng phân tích cảm xúc văn bản tiếng Việt sử dụng Fine-tuned PhoBERT với giao diện Streamlit.

## 📋 Mô tả Project

Hệ thống phân loại cảm xúc văn bản tiếng Việt thành 3 nhãn: **POSITIVE**, **NEGATIVE**, **NEUTRAL**.

### Tính năng chính:
- ✅ Fine-tuned PhoBERT model cho tiếng Việt
- ✅ Xử lý từ viết tắt (rat → rất, ko → không, etc.)
- ✅ Giao diện web thân thiện với Streamlit
- ✅ Lưu trữ lịch sử phân tích với SQLite
- ✅ Confidence score cho mỗi prediction
- ✅ Phân trang lịch sử với 5 records/trang

## 🏗️ Kiến trúc Project

### Luồng xử lý chính:
```
[Đầu vào: Câu tiếng Việt]
    ↓
[Component 1: Tiền xử lý]
    • Chuẩn hóa chữ thường
    • Thay thế từ viết tắt (abbreviation.csv)
    • Loại bỏ ký tự đặc biệt
    ↓
[Component 2: Fine-tuned PhoBERT]
    • Tokenize với PhoBERT tokenizer
    • Sentiment prediction với confidence
    • Nếu confidence < 0.5 → NEUTRAL
    ↓
[Component 3: Validation & Storage]
    • Kiểm tra độ dài câu (≥3 ký tự)
    • Lưu vào SQLite database
    • Trả về {text, sentiment, confidence}
    ↓
[Streamlit UI: Hiển thị kết quả]
```

### Cấu trúc files:
```
Vietnamese-Sentiment-Analysis/
├── app.py                          # Main Streamlit application
├── sentiment_model.py               # SentimentService class (PhoBERT wrapper)
├── database.py                      # SQLite operations
├── finetune_phobert.py              # Fine-tuning script cho PhoBERT
├── sentiment_data.csv               # Training dataset (8K+ samples)
├── abbreviation.csv                 # Text abbreviations mapping
├── requirements.txt                 # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                        # Documentation
```

### Tech Stack:
- **Frontend**: Streamlit
- **Model**: Fine-tuned PhoBERT (vinai/phobert-base)
- **Database**: SQLite
- **Processing**: PyTorch, Transformers, Pandas
- **Language**: Python 3.8+

## 🚀 Hướng dẫn Setup và Chạy

### 1. Clone repository:
```bash
git clone https://github.com/PhongKP/Vietnamese-Sentiment-Analysis.git
cd Vietnamese-Sentiment-Analysis
```

### 2. Tạo virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

### 4. Fine-tune model (BẮT BUỘC - chạy lần đầu):
```bash
python finetune_phobert.py
```
⏰ **Thời gian**: ~20-40 phút (CPU), ~10-15 phút (GPU)
📁 **Output**: Tạo folder `phobert-sentiment-final/` chứa fine-tuned model

### 5. Chạy ứng dụng:
```bash
streamlit run app.py
```

### 6. Truy cập: 
Mở browser tại `http://localhost:8501`

## 🔥 Fine-tuning Process

### ⚠️ **YÊU CẦU**: Phải chạy fine-tuning trước khi sử dụng app

### Quá trình Fine-tune PhoBERT:
1. **Load dữ liệu**: `sentiment_data.csv` (8K+ samples)
2. **Preprocessing**: Chuẩn hóa text + abbreviation expansion
3. **Data split**: 80% train, 20% validation
4. **Model**: vinai/phobert-base với 3 output labels
5. **Training**: 3 epochs, learning rate 2e-5, batch size 8
6. **Output**: Model được lưu trong `phobert-sentiment-final/`

### Training configuration:
- **Epochs**: 3
- **Learning rate**: 2e-5  
- **Batch size**: 8 (CPU), 16 (GPU)
- **Max sequence length**: 256
- **Optimizer**: AdamW với warmup
- **Early stopping**: Patience = 2 epochs

### Expected performance:
- **Validation accuracy**: ~85%+
- **Model size**: ~1.3GB
- **Inference time**: ~0.5-2s per sentence

## 📊 Database

- **Engine**: SQLite (`sentiment.db`)
- **Schema**: `sentiments(id, text, sentiment, timestamp)`
- **UI**: Hiển thị lịch sử với phân trang (5 records/page)
- **Auto-created**: Database tạo tự động khi chạy app lần đầu

## 🤖 Model Details

- **Base Model**: vinai/phobert-base
- **Fine-tuning**: Trained trên 8K+ Vietnamese sentiment samples
- **Labels**: POSITIVE, NEGATIVE, NEUTRAL
- **Confidence Threshold**: < 0.5 → mặc định NEUTRAL
- **Preprocessing**: Abbreviation expansion + text normalization

## 📁 Key Components

- **`finetune_phobert.py`**: Script fine-tune PhoBERT từ scratch
- **`SentimentService`**: Core model wrapper với preprocessing
- **`init_db()`**: Tạo SQLite schema tự động
- **`get_paginated_history()`**: Lấy lịch sử với phân trang

## 🧪 Development Workflow

1. **Clone repo**: `git clone ...`
2. **Setup environment**: Virtual env + dependencies
3. **Fine-tuning**: `python finetune_phobert.py` (BẮT BUỘC)
4. **Run app**: `streamlit run app.py`
5. **Test**: Thử nghiệm với các câu tiếng Việt

## ⚠️ Troubleshooting

### **Lỗi "Fine-tuned model not found":**
```
❌ Fine-tuned model not found at ./phobert-sentiment-final
```
**Giải pháp**: Chạy `python finetune_phobert.py` trước

### **Lỗi memory khi fine-tuning:**
- Giảm `batch_size` trong `finetune_phobert.py`
- Giảm `max_length` từ 256 xuống 128

### **Training quá chậm:**
- Sử dụng GPU nếu có
- Giảm `num_train_epochs` từ 3 xuống 2
