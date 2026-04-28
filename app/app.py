import os
from flask import Flask, render_template, request, session, redirect, url_for

from app.components.retriever import create_chain
from dotenv import load_dotenv

load_dotenv()

hf_token = os.environ.get("HF_TOKEN")

app = Flask(__name__)
app.secret_key = os.urandom()
