import random
import string
from flask import Flask, request, jsonify
import os
from shutil import rmtree
from traceback import print_exc
import requests

from recognize import recognize

app = Flask(__name__)

@app.route('/face-recognition', methods=['POST'])
def recognition():
    """
    Process the POST request and perform face recognition on the provided images.
        -> Create a temp directory
        -> Write the files to the temp directory according to extension
        -> Perform face recognition
        -> Delete the temp directory

    Args:
        request: The POST request object
            * image1: The first image [Required] ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'] [multipart/form-data]
            * image2: The second image [Required] ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'] [multipart/form-data]
    Returns:
        response: The response object
            {
                "result": "String" // "True" or "False"
            }
    """
    try:
        content_type = request.headers.get('Content-Type')

        if not content_type.startswith("multipart/form-data") and content_type != 'application/json':
            return jsonify({'statusCode': 422, 'error': 'Invalid content type. Please use multipart/form-data or application/json'})

        temp_dir = "temp" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        os.mkdir(temp_dir)
        
        if content_type == "application/json":
            image1 = request.json['image1']
            image1 = {"filename": image1.split("/")[-1], "url": image1}
            image2 = request.json['image2']
            image2 = {"filename": image2.split("/")[-1], "url": image2}
        else:
            if "image1" not in request.files or "image2" not in request.files:
                return jsonify({'statusCode': 422, 'error': 'Missing image1 or image2'})
            image1 = request.files['image1']
            image2 = request.files['image2']
        
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']
        for image in [image1, image2]:
            if content_type == "application/json":
                if image["filename"].lower().endswith(tuple(allowed_extensions)):
                    response = requests.get(image["url"])
                    if response.status_code == 200:
                        with open(os.path.join(temp_dir, image["filename"]), 'wb') as file:
                            file.write(response.content)
                    else:
                        return jsonify({'error': 'Invalid file url', "url": image["url"]})
                else:
                    return jsonify({'error': 'Invalid file type'})
            else:
                if image.filename.lower().endswith(tuple(allowed_extensions)):
                    image.save(os.path.join(temp_dir, image.filename))

        if content_type == "application/json":
            image1 = temp_dir + "/" + image1["filename"]
            image2 = temp_dir + "/" + image2["filename"]
        else:
            image1 = temp_dir + "/" + image1.filename
            image2 = temp_dir + "/" + image2.filename

        result = recognize(image1, image2)
        return jsonify({"result": str(result)})
    except Exception as e:
        print_exc()
        return jsonify({'statusCode': 500, 'error': 'Internal Server Error'})
    finally:
        rmtree(temp_dir)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True if os.getenv("Stage") == "dev" else False, port=5000)
