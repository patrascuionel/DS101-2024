import React, { useState } from 'react';
import axios from 'axios';
import './PredictionModal.css'; // We'll create this for styling

const PREDICT_API_URL = process.env.REACT_APP_PREDICT_API_URL || 'http://localhost:8000/predict'; // Fallback to /predict if env var is not set

const PredictionModal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    'Engine Size (cm3)': 2000,
    'Horse Power (HP)': 184,
    'Kilometers': 143000,
    'Year': 2012,
    'Is_xDrive': 1,
    'Fuel Type': 'Diesel',
    'Region': 'Bucuresti',
    'Engine_Badge': '320d',
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');

  const fuelTypes = ['Diesel', 'Benzina', 'Hibrid', 'Electric']; // Add more if needed
  const regions = ['Bucuresti', 'Ilfov', 'Center', 'North', 'South', 'East', 'West', 'Other_Region']; // From your notebook
  const engineBadges = ['320d', 'Unknown', '318d', '320i', '330e', 'Rarer Models', '318i', '316d', '330i']; // From your notebook

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? (checked ? 1 : 0) : (type === 'number' ? parseFloat(value) : value),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setPrediction(null);
    try {
      // The backend expects lists for each value
      const payload = Object.keys(formData).reduce((acc, key) => {
        acc[key] = [formData[key]];
        return acc;
      }, {});

      const response = await axios.post(PREDICT_API_URL, payload);
      setPrediction(response.data.predicted_price); // Adjust based on your API response structure
    } catch (err) {
      setError('Failed to get prediction. ' + (err.response?.data?.error || err.message));
    }
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Car Price Predictor</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Engine Size (cm3):</label>
            <input
              type="number"
              name="Engine Size (cm3)"
              value={formData['Engine Size (cm3)']}
              onChange={handleChange}
              min="1500"
              max="3500"
              required
            />
          </div>
          <div>
            <label>Horse Power (HP):</label>
            <input
              type="number"
              name="Horse Power (HP)"
              value={formData['Horse Power (HP)']}
              onChange={handleChange}
              min="120"
              max="600"
              required
            />
          </div>
          <div>
            <label>Kilometers:</label>
            <input
              type="number"
              name="Kilometers"
              value={formData['Kilometers']}
              onChange={handleChange}
              max="500000"
              required
            />
          </div>
          <div>
            <label>Year:</label>
            <input
              type="number"
              name="Year"
              value={formData['Year']}
              onChange={handleChange}
              min="1950"
              max="2025"
              required
            />
          </div>
          <div>
            <label>
              <input
                type="checkbox"
                name="Is_xDrive"
                checked={formData['Is_xDrive'] === 1}
                onChange={handleChange}
              />
              Is xDrive
            </label>
          </div>
          <div>
            <label>Fuel Type:</label>
            <select name="Fuel Type" value={formData['Fuel Type']} onChange={handleChange} required>
              {fuelTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Region:</label>
            <select name="Region" value={formData['Region']} onChange={handleChange} required>
              {regions.map((region) => (
                <option key={region} value={region}>
                  {region}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Engine Badge:</label>
            <select name="Engine_Badge" value={formData['Engine_Badge']} onChange={handleChange} required>
              {engineBadges.map((badge) => (
                <option key={badge} value={badge}>
                  {badge}
                </option>
              ))}
            </select>
          </div>
          <button type="submit">Predict Price</button>
          <button type="button" onClick={onClose}>Close</button>
        </form>
        {prediction !== null && (
          <div className="prediction-result">
            Predicted Price: €{parseFloat(prediction).toFixed(2)}
          </div>
        )}
        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
};

export default PredictionModal;