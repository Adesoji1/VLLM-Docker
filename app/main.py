# from flask import Flask, request, jsonify
# from vllm import LLM, SamplingParams

# app = Flask(__name__)

# # Load the model
# model_name = "Qwen/Qwen2-0.5B-Instruct"
# #Bfloat16 is only supported on GPUs with compute capability of at least 8.0. Your NVIDIA GeForce RTX 2060 GPU has compute capability 7.5. You can use float16 instead by explicitly setting the`dtype` flag in CLI, for example: --dtype=half.
# # llm = LLM(model=model_name, dtype="half")
# # llm = LLM(model=model_name)
# # llm = LLM(model=model_name, dtype="float32", device="cpu")
# llm = LLM(model=model_name, dtype="float16", device="cuda")



# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     if not data or "message" not in data:
#         return jsonify({"error": "Please provide a 'message' in JSON format."}), 400

#     # Generate a response
#     user_message = data["message"]
#     sampling_params = SamplingParams(temperature=0.7, top_p=0.95)
#     response = llm.generate([user_message], sampling_params=sampling_params)

#     return jsonify({"response": response[0].outputs[0].text})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)



from flask import Flask, request, jsonify
from vllm import LLM

app = Flask(__name__)
model_name = "Qwen/Qwen2-0.5B-Instruct"
llm = LLM(model=model_name, dtype="float16", device="cuda")


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        
        sampling_params = {"temperature": 0.8, "max_tokens": 150}  # Adjust parameters
        response = llm.generate([user_input], sampling_params=sampling_params)
        
        # Extract the generated text from the model's response
        generated_text = response[0].outputs[0].text.strip()
        return jsonify({"response": generated_text})
    
    except Exception as e:
        app.logger.error(f"Error in /chat: {e}")
        return jsonify({"error": "Internal Server Error"}), 500