from face_recognition import load_image_file, face_encodings, compare_faces

def recognize(image1, image2):
    try:
        # Load images
        image1 = load_image_file(image1)
        image2 = load_image_file(image2)
        # Encode faces
        face_encoding1 = face_encodings(image1)[0]
        face_encoding2 = face_encodings(image2)[0]
        # Compare face encodings
        results = compare_faces([face_encoding1], face_encoding2)
        # Output the result
        return results[0]
    except Exception as e:
        print({"error": str(e)})
        return None