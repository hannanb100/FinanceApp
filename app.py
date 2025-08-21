from flask import Flask, render_template, request, redirect, url_for, flash


def create_app() -> Flask:
	"""Factory to create and configure the Flask application.

	This keeps the app creation explicit and testable.
	"""
	app = Flask(__name__)
	# In a real app, keep the secret key secret. Used for flashing messages.
	app.config["SECRET_KEY"] = "dev-secret-key-change-me"

	@app.route("/", methods=["GET"]) 
	def index():
		"""Render the homepage with the financial goal form."""
		return render_template("index.html")

	@app.route("/results", methods=["POST"]) 
	def results():
		"""Handle form submission, validate input, and render the results page.

		Basic validation ensures required fields are present. If any field is blank,
		an error message is shown and the user is redirected back to the form.
		"""
		# Retrieve form data safely using .get to avoid KeyErrors
		financial_goal = request.form.get("financial_goal", "").strip()
		timeframe = request.form.get("timeframe", "").strip()
		current_savings = request.form.get("current_savings", "").strip()
		monthly_income = request.form.get("monthly_income", "").strip()
		risk_tolerance = request.form.get("risk_tolerance", "").strip()

		# Collect missing fields for helpful error feedback
		missing = []
		if not financial_goal:
			missing.append("What is your financial goal?")
		if not timeframe:
			missing.append("What is your target timeframe to achieve this goal?")
		if not current_savings:
			missing.append("What is your current savings?")
		if not monthly_income:
			missing.append("What is your monthly income?")
		if not risk_tolerance:
			missing.append("What is your risk tolerance?")

		if missing:
			# Flash a combined error message and send the user back to the form
			flash("Please complete all fields before submitting.")
			for field in missing:
				flash(f"Missing: {field}")
			return redirect(url_for("index"))

		# Optionally, further validate numeric inputs; for now just display values.
		return render_template(
			"results.html",
			financial_goal=financial_goal,
			timeframe=timeframe,
			current_savings=current_savings,
			monthly_income=monthly_income,
			risk_tolerance=risk_tolerance,
		)

	return app


if __name__ == "__main__":
	# Allow running via `python app.py` for local development
	app = create_app()
	# Debug mode provides auto-reload and better error pages during development
	app.run(host="0.0.0.0", port=5000, debug=True)

