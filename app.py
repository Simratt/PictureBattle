from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import base64

import os
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyse", methods=["POST"])
def analyse():
    try:
        # Get the uploaded images from the request
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Both images are required'}), 400
        
        image1 = request.files['image1']
        image2 = request.files['image2']
        
        # Validate file contents
        if image1.filename == '' or image2.filename == '':
            return jsonify({'error': 'No selected files'}), 400

        # Convert images to base64
        try:
            def encode_image(image):
                return base64.b64encode(image.read()).decode('utf-8')
            
            image1_base64 = encode_image(image1)
            image2_base64 = encode_image(image2)
        except Exception as e:
            app.logger.error(f"Error encoding images: {str(e)}")
            return jsonify({'error': 'Error processing images'}), 500

        prompt = """You are an enthusiastic Battle Analyst hosting an epic VERSUS showdown! 
        
        You've been given two challengers facing off against each other. Study both images carefully and provide:
        1. An exciting introduction of both contestants (their appearance, notable features, perceived strengths)
        3. Clearly give your dramatic prediction of the winner and why they would triumph
        4. in about 150 words, give a fun 'power rating' for each contestant (on a scale of 1-10) in categories like:
           - Strength
           - Speed
           - Special abilities
        
        Make it entertaining and dramatic, like you're a sports commentator calling the match of the century!
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image1_base64}",
                                },
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image2_base64}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return jsonify({'response': response.choices[0].message.content})
        except Exception as e:
            app.logger.error(f"OpenAI API error: {str(e)}")
            return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=False) 