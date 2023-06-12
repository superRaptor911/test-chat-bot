import { useEffect, useRef, useState } from "react";
import "./App.css";
import { api_askQuestion, api_getHistory } from "./api/bot";
import "./assets/gothic.ttf";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import hljs from "highlight.js";
import "highlight.js/styles/dark.css";
import skull from "./assets/skull2.png";

const ChatBox = ({ data }: { data: string[] }) => {
  return (
    <div className="chatbox">
      <div className="chatbox_user">
        <div className="chatbox_user_header">Thou:</div>
        <div className="chat_message">
          <ReactMarkdown children={data[0]} remarkPlugins={[remarkGfm]} />
        </div>
      </div>

      <div className="chatbox_bot">
        <div className="chatbox_bot_header">Machine:</div>
        <div className="chat_message">
          <ReactMarkdown children={data[1]} remarkPlugins={[remarkGfm]} />
        </div>
      </div>
    </div>
  );
};

function App() {
  const [chatHistory, setChatHistory] = useState<string[][]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const queryRef = useRef<HTMLTextAreaElement>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api_getHistory().then((res) => {
      setChatHistory(res.history);
    });
  }, []);

  useEffect(() => {
    hljs.highlightAll();
    scrollDown();
  }, [chatHistory]);

  const scrollDown = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSendClick = async () => {
    const query = queryRef.current?.value;
    if (query) {
      setIsProcessing(true);
      const res = await api_askQuestion(query);
      setChatHistory((prev) => [...prev, [query, res.answer]]);
      setIsProcessing(false);
    }
  };

  return (
    <>
      <div>
        <h2
          style={{
            fontFamily: "gothic",
            fontSize: 34,
          }}
        >
          Machine Spirit
        </h2>
        <div className="chat">
          {chatHistory.map((chat, idx) => (
            <ChatBox data={chat} key={idx} />
          ))}
          <div ref={chatEndRef} />
        </div>

        <div className="chat_query">
          <textarea className="chat_query_input" ref={queryRef} />
          {isProcessing ? (
            <input type="image" src={skull} className="chat_send_button_spin" />
          ) : (
            <input
              type="image"
              src={skull}
              className="chat_send_button"
              onClick={handleSendClick}
            />
          )}
        </div>
      </div>
    </>
  );
}

export default App;
