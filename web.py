from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_text", methods=["POST"])
def submit_text():
    data = request.json
    print("接收到的文字：", data.get("text"))
    return {"status": "success"}

@app.route("/rag_chat", methods=["POST"])
def rag_chat():
    data = request.json
    print("送出的文字到 RAG Chat：", data.get("query"))
    
    # 模擬向 6000 埠的 RAG Chat 發送請求
    response = requests.post(
        "http://localhost:6000/bot/ragChat",
        json={"query": data.get("query")},
        headers={"Content-Type": "application/json"}
    )
    
    rag_response = response.json()
    print("RAG Chat 回應：", rag_response['content'].strip("` \n,"))
    if("無法回答" in rag_response['content']):
        return jsonify({"rag_response": "無法回答"})
    # 解析 RAG Chat 回應並自動發送請求
    try:
        # 假設 RAG Chat 回應的格式為 {"content": "{\"route\":\"/temperature\",\"method\":\"GET\",\"data\":{}}"}
        inner_content = json.loads(rag_response['content'].strip("` \n,"))
        
        forwarded_response = None
        # 發送根據回應內容的請求
        if inner_content["method"] == "GET":
            forwarded_response = requests.get(
                "https://8772-2001-b400-e201-75a5-11a9-977a-5fde-5247.ngrok-free.app" + inner_content["route"],
                headers={"Content-Type": "application/json"}
            )
        elif inner_content["method"] == "POST":
            forwarded_response = requests.post(
                "https://8772-2001-b400-e201-75a5-11a9-977a-5fde-5247.ngrok-free.app" + inner_content["route"],
                json=inner_content["data"],
                headers={"Content-Type": "application/json"}
            )

        print("自動發送請求的回應：", forwarded_response.json())
        # 回傳被自動發送請求的結果
        return jsonify({
            "rag_response": rag_response,
            "forwarded_response": forwarded_response.json()
        })
    except Exception as e:
        print("解析或發送請求失敗：", str(e))
        return jsonify({"error": "Failed to process RAG Chat response."}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
