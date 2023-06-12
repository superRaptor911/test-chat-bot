const server = "http://localhost:8000";

type ChatHistory = {
  history: string[][];
};

type ChatResponse = {
  answer: string;
};
export const api_getHistory = async () => {
  const response = await fetch(`${server}/history`);
  const data = await response.json();

  return data as ChatHistory;
};

export const api_askQuestion = async (question: string) => {
  const response = await fetch(`${server}/question?q=${question}`);
  const data = await response.json();
  return data as ChatResponse;
};
