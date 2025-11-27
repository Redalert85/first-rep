import { useEffect, useRef } from "react";

const API_URL =
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent";

export const useAbortController = () => {
  const controllerRef = useRef(null);

  useEffect(() => {
    return () => controllerRef.current?.abort();
  }, []);

  const next = () => {
    controllerRef.current?.abort();
    controllerRef.current = new AbortController();
    return controllerRef.current.signal;
  };

  return next;
};

export async function callGemini(promptText, systemContext = "", abortSignal) {
  const apiKey = process.env.REACT_APP_GEMINI_API_KEY || "";
  const url = `${API_URL}?key=${apiKey}`;
  const fullPrompt = systemContext
    ? `${systemContext}\n\nUser Query: ${promptText}`
    : promptText;

  const payload = { contents: [{ parts: [{ text: fullPrompt }] }] };
  const delays = [750, 1500, 3000];

  for (let i = 0; i < delays.length; i++) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: abortSignal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
      return text?.trim() || "No response generated.";
    } catch (error) {
      if (abortSignal?.aborted) {
        throw new Error("Request was cancelled.");
      }

      if (i === delays.length - 1) {
        return `Error: ${error.message || "Connection failed."} Please try again.`;
      }
      await new Promise((resolve) => setTimeout(resolve, delays[i]));
    }
  }

  return "Error: Unable to reach the Gemini API.";
}
