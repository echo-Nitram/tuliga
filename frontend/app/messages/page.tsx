"use client";

import { useEffect, useState } from "react";

interface Conversation {
  id: number;
  title: string | null;
}

interface Message {
  id: number;
  sender: string;
  content: string;
  timestamp: string;
}

export default function MessagesPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<number | null>(
    null
  );
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [newTitle, setNewTitle] = useState("");
  const baseUrl = process.env.NEXT_PUBLIC_API_URL;

  async function fetchConversations() {
    try {
      const res = await fetch(`${baseUrl}/conversations`);
      if (res.ok) {
        const data = await res.json();
        setConversations(data);
        if (data.length > 0 && !activeConversationId) {
          setActiveConversationId(data[0].id);
        }
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function fetchMessages() {
    if (!activeConversationId) return;
    try {
      const res = await fetch(
        `${baseUrl}/conversations/${activeConversationId}/messages`
      );
      if (res.ok) {
        const data = await res.json();
        setMessages(data);
      }
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (!activeConversationId) return;
    fetchMessages();
    const interval = setInterval(fetchMessages, 5000);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeConversationId]);

  async function sendMessage() {
    if (!input || !activeConversationId) return;
    await fetch(`${baseUrl}/conversations/${activeConversationId}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender: "User", content: input }),
    });
    setInput("");
    fetchMessages();
  }

  async function createConversation() {
    const res = await fetch(`${baseUrl}/conversations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle || null }),
    });
    if (res.ok) {
      const convo = await res.json();
      setConversations((prev) => [...prev, convo]);
      setActiveConversationId(convo.id);
      setNewTitle("");
    }
  }

  return (
    <div>
      <h1>Messages</h1>
      <div>
        <label>
          Conversation:
          <select
            aria-label="conversation"
            value={activeConversationId ?? ""}
            onChange={(e) => setActiveConversationId(Number(e.target.value))}
          >
            {conversations.length === 0 ? (
              <option value="" disabled>
                No conversations
              </option>
            ) : (
              conversations.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.title || `Conversation ${c.id}`}
                </option>
              ))
            )}
          </select>
        </label>
      </div>
      <div>
        <input
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="New conversation title"
        />
        <button onClick={createConversation}>Create</button>
      </div>
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
