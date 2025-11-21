# app.py - minimal working version
from flask import Flask, render_template
from datetime import datetime
from data_analyzer import analyze_data

app = Flask(__name__)

@app.route('/')
def index():
    # Run the analysis
    metrics = analyze_data()

    # If there’s an error from the analyzer, show error page
    if 'error' in metrics:
        return render_template('error.html', message=metrics['error']), 503

    # Format timestamp for display
    timestamp = metrics.get('last_updated_ts', 0)
    metrics['last_updated_gmt'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')

    # Now metrics only has min/max station info and last_updated
    return render_template('dashboard.html', metrics=metrics)

@app.route('/api/metrics')
def api_metrics():
    # API endpoint for raw metrics
    return analyze_data()

if __name__ == '__main__':
    app.run(debug=True)

