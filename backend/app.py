import os
import sys
import shutil
import subprocess
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_FOLDER = os.path.join(os.path.dirname(BASE_DIR), "frontend")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESULT_FOLDER = os.path.join(BASE_DIR, "results")
MODEL_PATH    = os.path.join(BASE_DIR, "model", "sds_yolo_best.pt")
YOLOV5_FOLDER = os.path.join(BASE_DIR, "yolov5")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Draw numbered badges on the YOLO annotated image ─────────────────────────
#
# After YOLO saves its annotated image (boxes + class labels), we load it with
# OpenCV and stamp a small numbered circle badge (①②③…) at the top-left corner
# of every bounding box.  The number matches the row in the Detection Log, so
# the user can instantly identify which object is which.

BADGE_BG   = (255, 255, 255)   # white fill  (BGR)
BADGE_TEXT = (20,  20,  20)    # near-black number


def draw_numbered_detections(image_path, label_path, output_path):
    """
    Load the YOLO-annotated image, overlay a numbered badge on each detection,
    and write the result to output_path.

    label_path: YOLO .txt  —  class  cx  cy  w  h  conf  (all normalised 0-1)
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"[NUMBER] Cannot read image: {image_path}")
        shutil.copy(image_path, output_path)
        return

    h, w = img.shape[:2]

    if not label_path or not os.path.exists(label_path):
        print(f"[NUMBER] No label file — copying image as-is")
        shutil.copy(image_path, output_path)
        return

    with open(label_path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    for idx, line in enumerate(lines, start=1):
        parts = line.split()
        if len(parts) < 5:
            continue

        # YOLO normalised bbox → pixel coords
        cx = float(parts[1]);  cy = float(parts[2])
        bw = float(parts[3]);  bh = float(parts[4])

        x1 = max(0, int((cx - bw / 2) * w))
        y1 = max(0, int((cy - bh / 2) * h))

        # Badge: circle centred just inside the top-left corner of the box
        r        = 14
        badge_cx = min(x1 + r + 3, w - r - 2)
        badge_cy = min(y1 + r + 3, h - r - 2)

        # Black outline → white fill → number
        cv2.circle(img, (badge_cx, badge_cy), r + 2, (0, 0, 0),  -1)
        cv2.circle(img, (badge_cx, badge_cy), r,     BADGE_BG,   -1)

        num_str    = str(idx)
        font       = cv2.FONT_HERSHEY_SIMPLEX
        scale      = 0.45 if idx < 10 else 0.38
        thickness  = 1
        (tw, th), _ = cv2.getTextSize(num_str, font, scale, thickness)
        cv2.putText(img, num_str,
                    (badge_cx - tw // 2, badge_cy + th // 2),
                    font, scale, BADGE_TEXT, thickness, cv2.LINE_AA)

    cv2.imwrite(output_path, img)
    print(f"[NUMBER] Numbered image saved → {output_path}")


# ─── Frontend ─────────────────────────────────────────────────

@app.route("/")
def frontend_home():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/style.css")
def frontend_css():
    return send_from_directory(FRONTEND_FOLDER, "style.css")

@app.route("/script.js")
def frontend_js():
    return send_from_directory(FRONTEND_FOLDER, "script.js")

@app.route("/api/status")
def api_status():
    return jsonify({"success": True, "message": "SDS-YOLO backend running"})


# ─── Predict ──────────────────────────────────────────────────

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "message": "No image file uploaded"}), 400

        image = request.files["image"]

        if image.filename == "":
            return jsonify({"success": False, "message": "No image selected"}), 400

        if not allowed_file(image.filename):
            return jsonify({"success": False, "message": "Only JPG, JPEG, PNG allowed"}), 400

        if not os.path.exists(MODEL_PATH):
            return jsonify({"success": False, "message": "Model not found", "path": MODEL_PATH}), 500

        detect_py = os.path.join(YOLOV5_FOLDER, "detect.py")
        if not os.path.exists(detect_py):
            return jsonify({"success": False, "message": "detect.py not found"}), 500

        # Clean previous run
        shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
        shutil.rmtree(RESULT_FOLDER, ignore_errors=True)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(RESULT_FOLDER, exist_ok=True)

        # Save upload
        ext            = image.filename.rsplit(".", 1)[1].lower()
        saved_filename = f"uploaded_image.{ext}"
        image_path     = os.path.join(UPLOAD_FOLDER, saved_filename)
        image.save(image_path)

        output_dir = os.path.join(RESULT_FOLDER, "output")

        command = [
            sys.executable, detect_py,
            "--weights",        MODEL_PATH,
            "--conf", "0.45",
            "--iou-thres", "0.25",
            "--max-det", "300",
            "--source",         image_path,
            "--project",        RESULT_FOLDER,
            "--name",           "output",
            "--exist-ok",
            "--save-txt",
            "--save-conf",
            "--line-thickness", "2",
        ]

        print("\n[SDS-YOLO] Running:", " ".join(command))
        process = subprocess.run(command, capture_output=True, text=True, cwd=YOLOV5_FOLDER)
        print("[STDOUT]", process.stdout)
        print("[STDERR]", process.stderr)

        if process.returncode != 0:
            return jsonify({
                "success": False, "message": "YOLO failed",
                "stdout": process.stdout, "stderr": process.stderr
            }), 500

        # Find YOLO output image
        yolo_image_path = os.path.join(output_dir, saved_filename)
        if not os.path.exists(yolo_image_path):
            found = [
                os.path.join(r, f)
                for r, _, files in os.walk(output_dir)
                for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ]
            if found:
                yolo_image_path = found[0]
                saved_filename  = os.path.basename(yolo_image_path)
            else:
                return jsonify({
                    "success": False, "message": "Output image not found",
                    "stdout": process.stdout, "stderr": process.stderr
                }), 500

        print(f"[SDS-YOLO] YOLO image: {yolo_image_path}")

        # Find label file
        label_stem = os.path.splitext(saved_filename)[0]
        label_file = os.path.join(output_dir, "labels", f"{label_stem}.txt")
        if not os.path.exists(label_file):
            label_file = os.path.join(output_dir, "labels", "uploaded_image.txt")

        # Parse detections
        detections = []
        if os.path.exists(label_file):
            with open(label_file, "r") as f:
                lines = [l.strip() for l in f if l.strip()]
            for idx, line in enumerate(lines, start=1):
                parts = line.split()
                if len(parts) >= 6:
                    class_id   = int(float(parts[0]))
                    confidence = float(parts[5])
                    class_name = {0: "Dust", 1: "Bird-Droppings"}.get(class_id, "Unknown")
                    detections.append({
                        "number":     idx,
                        "class_id":   class_id,
                        "class_name": class_name,
                        "confidence": round(confidence, 2)
                    })

        # Draw numbered badges on top of YOLO output image
        numbered_filename   = f"numbered_{saved_filename}"
        numbered_image_path = os.path.join(output_dir, numbered_filename)

        draw_numbered_detections(
            image_path  = yolo_image_path,
            label_path  = label_file,
            output_path = numbered_image_path
        )

        detected = len(detections) > 0

        return jsonify({
            "success":        True,
            "detected":       detected,
            "detected_count": len(detections),
            "detections":     detections,
            "message":        "Soiling detected in this panel" if detected else "No soiling detected",
            "result_image":   f"/result-image/{numbered_filename}"
        })

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


# ─── Serve result image with no-cache ─────────────────────────

@app.route("/result-image/<path:filename>")
def serve_result_image(filename):
    file_path = os.path.join(RESULT_FOLDER, "output", filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Image not found"}), 404
    resp = send_file(file_path, mimetype="image/jpeg", as_attachment=False)
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"]        = "no-cache"
    resp.headers["Expires"]       = "0"
    return resp


@app.route("/results/<path:filename>")
def serve_result_legacy(filename):
    return send_from_directory(RESULT_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)