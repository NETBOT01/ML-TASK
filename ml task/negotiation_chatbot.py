from google.api_core import retry
from google.cloud import aiplatform_v1

# Replace with your actual Gemini API key or set it as an environment variable
# For example: os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
api_key = "AIzaSyCMzh_HCS9pnJfeQB"
"

async def chat_with_gemini(prompt):
    client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    client = aiplatform_v1.PredictionServiceClient(client_options=client_options)

    endpoint = f"projects/gcp-project-id/locations/us-central1/publishers/google/models/gemini-pro"  # Replace with your Gemini model endpoint
    parameters = aiplatform_v1.GenerateTextRequest.Parameters(temperature=0.7, max_output_tokens=50)
    request = aiplatform_v1.GenerateTextRequest(
        model=endpoint,
        prompt={"text": prompt},
        parameters=parameters,
    )

    @retry.Retry()
    def call_generate_text():
        return client.generate_text(request=request)

    response = call_generate_text()

    return response.predictions[0].content
