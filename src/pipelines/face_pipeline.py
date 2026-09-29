

import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() 


    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings= []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #128 embedding

        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    try:
        student_db = get_all_students()
    except Exception:
        return None

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        sid = student.get('student_id')
        if embedding and sid is not None:
            X.append(np.array(embedding))
            y.append(sid)

    if len(X) == 0:
        return None

    unique_classes = set(y)
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    if len(unique_classes) >= 2:
        try:
            clf.fit(X, y)
        except ValueError:
            pass

    return {'clf': clf, 'X': X, 'y': y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    try:
        encodings = get_face_embeddings(class_image_np)
    except Exception:
        encodings = []

    detected_student = {}

    model_data = get_trained_model()

    if not model_data or not isinstance(model_data, dict):
        return detected_student, [], len(encodings)

    clf = model_data.get('clf')
    X_train = model_data.get('X', [])
    y_train = model_data.get('y', [])

    all_students = sorted(list(set(y_train)))
    if not all_students:
        return detected_student, [], len(encodings)

    for encoding in encodings:
        if len(all_students) >= 2 and hasattr(clf, "classes_"):
            try:
                predicted_id = int(clf.predict([encoding])[0])
            except Exception:
                predicted_id = int(all_students[0])
        else:
            predicted_id = int(all_students[0])

        if predicted_id in y_train:
            student_embedding = X_train[y_train.index(predicted_id)]
            best_match_score = np.linalg.norm(student_embedding - encoding)

            resemblance_threshold = 0.6

            if best_match_score <= resemblance_threshold:
                detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)
