"use client";

import { useEffect, useState } from "react";

interface Message {
  id: number;
  sender: string;
  content: string;
  timestamp: string;
}

export default function MessagesPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const baseUrl = process.env.NEXT_PUBLIC_API_URL;

  async function fetchMessages() {
    try {
      const res = await fetch(`${baseUrl}/conversations/1/messages`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data);
      }
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    fetchMessages();
    const interval = setInterval(fetchMessages, 5000);
    return () => clearInterval(interval);
  }, []);

  async function sendMessage() {
    if (!input) return;
    await fetch(`${baseUrl}/conversations/1/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender: "User", content: input }),
    });
    setInput("");
    fetchMessages();
  }

  return (
    <div>
      <h1>Messages</h1>
      <ul>
        {messages.map((m) => (
          <li key={m.id}>
            <strong>{m.sender}:</strong> {m.content}
          </li>
        ))}
      </ul>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type message"
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
