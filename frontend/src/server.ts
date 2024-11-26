export interface ChatMessageResponse {
  id?: string;
  question?: string;
  answer: string;
  reasoning?: string;
}

function createChatMessageResponse(message: string): ChatMessageResponse {
  return { answer: message };
}

export const getResponse = async (
  message: string,
): Promise<ChatMessageResponse> => {
  if (message == 'healthcheck') {
    return checkBackendHealth();
  } else {
    return callChatEndpoint(message);
  }
};

const unhappyHealthcheckResponse = createChatMessageResponse(
  'InferESG healthcheck: backend is unhealthy. Unable to healthcheck Neo4J. Please check the README files for further guidance',
);

const checkBackendHealth = async (): Promise<ChatMessageResponse> => {
  return await fetch(`${process.env.BACKEND_URL}/health`)
    .then((response) => response.json())
    .then((responseJson) => {
      return createChatMessageResponse(responseJson);
    })
    .catch((error) => {
      console.error('Error making REST call to /health: ', error);
      return unhappyHealthcheckResponse;
    });
};

const unhappyChatResponse = createChatMessageResponse(
  'I\'m sorry, but I was unable to process your message. Please check the status of the service using the phrase "healthcheck"',
);

const callChatEndpoint = async (
  message: string,
): Promise<ChatMessageResponse> => {
  return await fetch(`${process.env.BACKEND_URL}/chat?utterance=${message}`, {
    credentials: 'include',
  })
    .then((response) => {
      if (!response.ok) {
        console.log('error found');
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response;
    })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error making REST call to /chat: ', error);
      return unhappyChatResponse;
    });
};

export const getSuggestions = async (): Promise<string[]> => {
  return await fetch(`${process.env.BACKEND_URL}/suggestions`, {
    credentials: 'include',
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error making REST call to /suggestions: ', error);
      return [];
    });
};

export const resetChat = async (): Promise<Response> => {
  return await fetch(`${process.env.BACKEND_URL}/chat`, {
    credentials: 'include',
    method: 'DELETE',
  });
};

export const uploadFileToServer = async (
  file: File,
): Promise<{ filename: string; id: string }> => {
  const formData = new FormData();
  formData.append('file', file);

  return await fetch(`${process.env.BACKEND_URL}/report`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Upload failed with status : ${response.status}`);
      }
      return response.json();
    })
    .catch((error) => {
      console.error('Error uploading file:', error);
      throw error;
    });
};
