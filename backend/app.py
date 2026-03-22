from flask import Flask, request, jsonify
from flask_cors import CORS
from validation import validate_application
from intelligence import score_application
from sheets import write_to_sheet
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "AdmitGuard V2 Backend is running"})

@app.route("/validate", methods=["POST"])
def validate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Step 1: Run validation
        validation_result = validate_application(data)

        # Step 2: If Tier 1 errors exist → reject
        if validation_result["tier1"]:
            return jsonify({
                "status": "rejected",
                "errors": validation_result["tier1"]
            }), 400

        # Step 3: Get Tier 2 flags
        flags = validation_result["tier2"]

        # Step 4: Run intelligence layer
        score_data = score_application(data)

        # Step 5: Write to Google Sheet
        try:
            write_to_sheet(data, flags, score_data)
        except Exception as sheet_error:
            import traceback
            print(f"Sheet write failed: {sheet_error}")
            print(f"Full traceback: {traceback.format_exc()}")
            # Don't fail the whole request if sheet write fails

        return jsonify({
            "status": "accepted",
            "flags": flags,
            "score": score_data["risk_score"],
            "category": score_data["category"],
            "experience_bucket": score_data["experience_bucket"],
            "total_experience_months": score_data["total_experience_months"]
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)