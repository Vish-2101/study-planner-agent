from flask import Flask, render_template, request, jsonify
from main import run_study_planner

app = Flask(__name__)

@app.route('/')
def home():
    """Serve the index.html page."""
    return render_template('index.html')

@app.route('/api/plan', methods=['POST'])
def plan():
    """API endpoint to trigger the AI agent."""
    data = request.json
    subjects = data.get('subjects') # Expected to be a list of objects now
    days = data.get('days')
    hours = data.get('hours')

    if not subjects or not isinstance(subjects, list) or len(subjects) == 0:
        return jsonify({'error': 'Please provide at least one valid subject.'}), 400
        
    if not days or not hours:
        return jsonify({'error': 'Missing days or hours fields.'}), 400

    try:
        days = int(days)
        hours = int(hours)
        
        # Run the agent
        result = run_study_planner(subjects, days, hours)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except ValueError:
        return jsonify({'error': 'Days and Study Hours must be valid numbers.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
