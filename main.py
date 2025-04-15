from flask import Flask, render_template, request, jsonify


from thruster import Thruster, Pump

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        # Get user inputs
        n_thruster = int(request.json["n_thruster"])
        target_efficiency = float(request.json["target_efficiency"])
        thruster_quality = int(request.json["thruster_quality"])
        pump_quality = int(request.json["pump_quality"])
        max_period = int(request.json["max_period"])
        
        # Validate inputs
        if n_thruster <= 0:
            raise ValueError("Number of thrusters must be greater than 0.")
        if target_efficiency <= 0 or target_efficiency > 1:
            raise ValueError("Target efficiency must be between 0 and 1.")
        if thruster_quality < 0 or thruster_quality > 4:
            raise ValueError("Thruster quality must be between 0 and 4.")
        if pump_quality < 0 or pump_quality > 4:
            raise ValueError("Pump quality must be between 0 and 4.")
        if max_period <= 2:
            raise ValueError("Clock period must be greater than 2.")
        

        # Perform computations
        consumption_per_thruster = Thruster.consumption_from_efficiency(target_efficiency, thruster_quality)
        consumption = n_thruster * consumption_per_thruster
        n_pump, period, on_ticks, ticks_error = Pump.parameters(consumption, pump_quality, max_period=max_period)
        off_ticks = period - on_ticks

        # Prepare results
        results = {
    
            "consumption_per_thruster": consumption_per_thruster,
            "relative_thrust": Thruster.relative_thrust_from_consumption(consumption_per_thruster, thruster_quality),
            "total_consumption": consumption,
            "max_period": max_period,
            "n_pump": n_pump,
            "period": period,
            "on_ticks": on_ticks,
            "off_ticks": off_ticks,
            "ticks_error": ticks_error,
        }

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)