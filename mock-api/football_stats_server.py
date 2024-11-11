from datetime import datetime
from flask import Flask, jsonify
import random
import uuid

app = Flask(__name__)


@app.route("/data", methods=["GET"])
def get_player_updates():
    """Create random players with new performance ratings"""
    data = {
        "player_id": uuid.uuid4(),
        "match_id": random.randint(10, 99),
        "timestamp": datetime.now(),
        "new_rating": random.uniform(10.0, 100.0),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
