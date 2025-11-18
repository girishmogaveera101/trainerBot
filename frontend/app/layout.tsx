import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TrainerBot",
  description: "A Retrieval-Augmented Generation (RAG) chatbot for gym and fitness questions, powered by Groq's Llama 3.1 and semantic search",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
