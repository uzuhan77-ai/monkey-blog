import request from "../utils/request";

export function ApiAIWritingAssistant(data) {
  return request.post("/ai/writing-assistant/", data,{
    timeout:120000,
  });
}