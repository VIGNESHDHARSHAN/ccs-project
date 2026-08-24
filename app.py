import hashlib
import os

from flask import Flask, render_template, request, session


app = Flask(__name__)
app.secret_key = os.environ.get("SHA_SHIELD_SECRET", "local-development-secret")


def calculate_hash(upload):
    sha512 = hashlib.sha512()
    while chunk := upload.read(1024 * 1024):
        sha512.update(chunk)
    return sha512.hexdigest()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        upload = request.files.get("image")
        action = request.form.get("action")

        if not upload or not upload.filename:
            result = {"kind": "error", "title": "No file selected", "message": "Choose an image or file before continuing."}
        elif action == "register":
            digest = calculate_hash(upload)
            session["registered_hash"] = digest
            session["registered_name"] = upload.filename
            result = {
                "kind": "success",
                "title": "Original registered",
                "message": f"{upload.filename} is now your reference file.",
                "digest": digest,
            }
        elif action == "verify":
            registered_hash = session.get("registered_hash")
            if not registered_hash:
                result = {"kind": "error", "title": "Register an original first", "message": "Your reference digest is not set yet."}
            else:
                digest = calculate_hash(upload)
                is_authentic = digest == registered_hash
                result = {
                    "kind": "authentic" if is_authentic else "tampered",
                    "title": "Authentic file" if is_authentic else "Tampering detected",
                    "message": "The SHA-512 digest matches your reference." if is_authentic else "The SHA-512 digest does not match your reference.",
                    "digest": digest,
                }

    return render_template(
        "index.html",
        result=result,
        registered_name=session.get("registered_name"),
        registered_hash=session.get("registered_hash"),
    )


if __name__ == "__main__":
    app.run(debug=True)