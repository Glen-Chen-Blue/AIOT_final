let isRecording = false;
let recognition;
let silenceTimeout;

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  // recognition.lang = "en-US";
  recognition.lang = "zh-TW";

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    document.getElementById("transcript").textContent = transcript;
    document.getElementById("confirmButton").disabled = false;
    resetSilenceTimer();
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
  };

  recognition.onend = () => {
    if (isRecording) {
      recognition.start();
    }
  };
} else {
  alert("您的瀏覽器不支援 Web Speech API！");
}

document.getElementById("recordButton").addEventListener("click", toggleRecording);
document.getElementById("confirmButton").addEventListener("click", sendToRagChat);

function toggleRecording() {
  const button = document.getElementById("recordButton");
  if (isRecording) {
    button.textContent = "錄音";
    stopRecognition();
  } else {
    button.textContent = "停止";
    startRecognition();
  }
  isRecording = !isRecording;
}

function startRecognition() {
  recognition.start();
  resetSilenceTimer();
}

function stopRecognition() {
  recognition.stop();
  clearTimeout(silenceTimeout);
}

function resetSilenceTimer() {
  clearTimeout(silenceTimeout);
  silenceTimeout = setTimeout(() => {
    console.log("三秒無語音輸入，自動停止錄音。");
    const button = document.getElementById("recordButton");
    button.textContent = "錄音";
    stopRecognition();
    isRecording = false;
  }, 2000);
}

function sendToRagChat() {
  const transcript = document.getElementById("transcript").textContent;
  if (transcript) {
    fetch("/rag_chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: transcript }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.rag_response) {
          console.log("RAG Chat 回應：", data.rag_response.content);
          const outputDiv = document.getElementById("transcript");
          outputDiv.textContent = `AI 回應：${data.rag_response.content}`;

          if (data.forwarded_response) {
            console.log("自動請求回應：", data.forwarded_response);
            const forwardOutputDiv = document.getElementById("forwardedResponse");
            forwardOutputDiv.textContent = `自動請求回應：${JSON.stringify(data.forwarded_response)}`;
          }
        }
      })
      .catch((error) => {
        console.error("文字傳送到 RAG Chat 或自動請求失敗：", error);
      });
  }
}
