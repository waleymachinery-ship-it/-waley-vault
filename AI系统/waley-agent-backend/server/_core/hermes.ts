import { ENV } from "./env";

export type Role = "system" | "user" | "assistant";

export type Message = {
  role: Role;
  content: string;
};

export type InvokeParams = {
  messages: Message[];
  model?: string;
  maxTokens?: number;
};

export type InvokeResult = {
  id: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: {
      role: Role;
      content: string;
    };
    finish_reason: string | null;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
};

const resolveApiUrl = () => {
  if (ENV.hermesApiUrl && ENV.hermesApiUrl.trim().length > 0) {
    return `${ENV.hermesApiUrl.replace(/\/$/, "")}/v1/chat/completions`;
  }
  // Default to cloud Hermes
  return "http://106.53.207.188/hermes/v1/chat/completions";
};

const resolveApiKey = () => {
  if (ENV.hermesApiKey) {
    return ENV.hermesApiKey;
  }
  // Default Hermes API key
  return "hermes-api-key-2026";
};

export async function invokeHermes(params: InvokeParams): Promise<InvokeResult> {
  const { messages, model = "MiniMax-M2.7", maxTokens = 32768 } = params;

  const payload = {
    model,
    messages: messages.map((m) => ({
      role: m.role,
      content: m.content,
    })),
    max_tokens: maxTokens,
  };

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 120000);

  let response: Response;
  try {
    response = await fetch(resolveApiUrl(), {
      method: "POST",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${resolveApiKey()}`,
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
  } catch (err) {
    clearTimeout(timeoutId);
    if (err instanceof Error && err.name === "AbortError") {
      throw new Error(`Hermes invoke timeout after 120s`);
    }
    throw err;
  }

  clearTimeout(timeoutId);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Hermes invoke failed: ${response.status} ${response.statusText} - ${errorText}`
    );
  }

  return (await response.json()) as InvokeResult;
}
