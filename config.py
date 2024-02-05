from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

from utils import get_debug_logger


# Setting up FAST API handler classes
app = FastAPI(
    title="NER Service", description="API for getting privacy entities", version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setting up the NER Model
model_name = "Isotonic/distilbert_finetuned_ai4privacy_v2"
model = AutoModelForTokenClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

pipe = pipeline(
    task="ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple"
)

# Setting up logger
logging = get_debug_logger()
