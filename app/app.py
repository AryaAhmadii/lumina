import os
from markupsafe import Markup
from flask import Flask, render_template, request, session, redirect, url_for

from app.components.retriever import create_chain
from dotenv import load_dotenv

load_dotenv()

hf_token = os.environ.get("HF_TOKEN")

app = Flask(__name__)
app.secret_key = os.urandom(24)


# replacing \n in text with html break
def nl2br(text):
  return Markup(text.replace("\n", "<br>\n"))
app.jinja_env.filters["nl2br"] = nl2br

# routing
@app.route("/", methods=["GET", "POST"])
def index():
  if "messages" not in session:
    session["messages"] = []

  if request.method == "POST":
    input = request.form.get("prompt")
    if input:
      messages = session["messages"]
      messages.append({
        "role": "user",
        "content": input
      })
      session["messages"] = messages


      chain = create_chain()
      response = chain.invoke({"query": input})
      res = response.get("result", "no output")
      messages.append({"role": "assistant", "content": res})

    return redirect(url_for("index"))
  return render_template("index.html", messages = session.get("messages" , []))


@app.route("/clear")
def clear():
    session.pop("messages", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=5000 , debug=False , use_reloader = False)
