"use client"

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send } from 'lucide-react';
const BACKEND_URL: string = process.env.NEXT_PUBLIC_BACKEND_URL || "";

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

interface ApiResponse {
  question: string;
  answer: string;
  sources: string[];
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hey! I\'m your gym & fitness assistant. Ask me anything about workouts, nutrition, or muscle building!'
    }
  ]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const askModel = async (): Promise<void> => {
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/ask`, {
      // const response = await fetch(`http://localhost:7860/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input }),
      });

      const data: ApiResponse = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer || 'Sorry, I couldn\'t generate a response.',
        sources: data.sources || []
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error:', err);
      const errorMessage: Message = {
        role: 'assistant',
        content: '❌ Sorry, I couldn\'t connect to the server. Please make sure the API is running on http://localhost:7860'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      askModel();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-black">
      {/* Header */}
      <div className="bg-black flex justify-start pl-[5%] border-b border-gray-700 py-4 shadow-xl">
          <div>
            <h1 className="text-3xl font-bold text-blue-400">TrainerBot</h1>
            <p className="text-md text-gray-400">Powered by Groq & RAG</p>
          </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 bg-black overflow-y-auto px-4 py-6 pb-[10%]">
        <div className="md:mx-[15%] space-y-6">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
            >
              {msg.role === 'assistant' && (
                <div className="md:w-20 md:h-20 h-max rounded-full bg-gray-900 flex items-center justify-center mt-1">
                  <span className="text-4xl">🤖</span>
                </div>
              )}

              <div
                className={`max-w-[80%] rounded-2xl px-5 py-3 text-xl md:text-2xl ${msg.role === 'user'
                    ? 'bg-gray-900 text-gray-100'
                    : 'bg-gray-1000 border border-gray-800 text-gray-300 '
                  }`}
              >
                <div className="prose space-y-5 prose-invert max-w-none prose-p:my-2 prose-ul:my-2 prose-li:my-1 prose-headings:mt-3 prose-headings:mb-2">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>

              {msg.role === 'user' && (
                <div className="md:w-15 md:h-15 rounded-full bg-gray-500 flex items-center justify-center mt-1">
                  <span className="text-4xl">👤</span>
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-lg bg-red-400 flex items-center justify-center">
                <span className="text-lg">🤖</span>
              </div>
              <div className="bg-gray-800 border border-gray-700 rounded-2xl px-5 py-3">
                <div className="flex gap-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-transparent fixed bottom-5 md:bottom-10 flex justify-center w-full md:h-[8%] h-[6%] items-center border-0 border-blue-300">
        <div className="md:w-[60%] w-[90%] flex justify-center h-full items-center bg-transparent">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me.."
                className="md:w-[90%] w-[80%] md:pt-6 pt-3 h-full pl-10 bg-black md:text-3xl text-xl text-white rounded-l-full border border-blue-500"
                rows={1}
                disabled={isLoading}
              />
            <div className="bg-blue-500  md:w-[10%] w-[20%] rounded-r-full h-full justify-center items-center flex">
              <Send
              onClick={askModel}
              className="md:size-10 text-white"
            />
            </div>
        </div>
      </div>
    </div>
  );
}