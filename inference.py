from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="wcDKxxCya6kJIpda6sK2"
)

result = CLIENT.infer(your_image.jpg, model_id="eye-diseases-sonmr/1")