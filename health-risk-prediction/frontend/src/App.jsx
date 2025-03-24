import { useState } from "react";
import axios from "axios";
import {
  Container,
  TextField,
  Button,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Card,
  CardContent,
  CircularProgress,
} from "@mui/material";
import HealthAndSafetyIcon from "@mui/icons-material/HealthAndSafety";

function App() {
  const [formData, setFormData] = useState({
    age: "",
    family_history: "No",
    smoking: "Non-Smoker",
    alcohol: "Non-Drinker",
    diet_score: "",
    physical_activity: "",
    symptom_score: "",
    mri_abnormality: "Normal",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [validationError, setValidationError] = useState("");

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Convert to number for validation
    const numericValue = Number(value);

    // Validation for Diet Score, Physical Activity, and Symptom Score (1-10)
    if (["diet_score", "physical_activity", "symptom_score"].includes(name)) {
      if (numericValue < 1 || numericValue > 10) {
        setValidationError(`${name.replace("_", " ")} must be between 1 and 10`);
        return;
      } else {
        setValidationError("");
      }
    }

    setFormData({ ...formData, [name]: value });
  };

  // Submit form data to Flask API
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Prevent submission if validation error exists
    if (validationError) return;

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", formData, {
        headers: { "Content-Type": "application/json" },
      });
      setPrediction(response.data.risk_level);
    } catch (err) {
      setError(err.response?.data?.error || "Error fetching prediction. Ensure the backend is running.");
    }

    setLoading(false);
  };

  return (
    <Container maxWidth="md" className="app-container">
      <Card className="glassmorphic-card">
        <CardContent>
          <div className="title-container">
            <HealthAndSafetyIcon className="icon" fontSize="large" />
            <Typography variant="h4" className="title" sx={{ color: "blue" }}>
              Health Risk Prediction
            </Typography>
          </div>

          <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              {Object.keys(formData).map((key) => (
                <Grid item xs={12} sm={6} key={key}>
                  {["family_history", "smoking", "alcohol", "mri_abnormality"].includes(key) ? (
                    <FormControl fullWidth variant="outlined">
                      <InputLabel>{key.replace("_", " ").toUpperCase()}</InputLabel>
                      <Select name={key} value={formData[key]} onChange={handleChange} label={key.replace("_", " ")}>
                        {key === "mri_abnormality"
                          ? ["Normal", "Abnormal"].map((option) => (
                              <MenuItem key={option} value={option}>
                                {option}
                              </MenuItem>
                            ))
                          : key === "family_history"
                          ? ["Yes", "No"].map((option) => (
                              <MenuItem key={option} value={option}>
                                {option}
                              </MenuItem>
                            ))
                          : key === "smoking"
                          ? ["Smoker", "Non-Smoker"].map((option) => (
                              <MenuItem key={option} value={option}>
                                {option}
                              </MenuItem>
                            ))
                          : key === "alcohol"
                          ? ["Drinker", "Non-Drinker"].map((option) => (
                              <MenuItem key={option} value={option}>
                                {option}
                              </MenuItem>
                            ))
                          : null}
                      </Select>
                    </FormControl>
                  ) : (
                    <TextField
                      fullWidth
                      variant="outlined"
                      type="number"
                      name={key}
                      label={key.replace("_", " ").toUpperCase()}
                      value={formData[key]}
                      onChange={handleChange}
                      required
                      inputProps={["diet_score", "physical_activity", "symptom_score"].includes(key) ? { min: 1, max: 10 } : {}}
                    />
                  )}
                </Grid>
              ))}
            </Grid>

            {/* Show validation error if any */}
            {validationError && (
              <Typography color="error" style={{ marginTop: "10px" }}>
                {validationError}
              </Typography>
            )}

            <Button
              type="submit"
              className="btn"
              variant="contained"
              color="primary"
              fullWidth
              style={{ marginTop: "20px" }}
              disabled={loading || validationError}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : "Predict"}
            </Button>
          </form>

          {prediction !== null && (
            <Typography variant="h6" className="result" sx={{ paddingTop: 4 }}>
              Predicted Risk Level: <strong>{prediction}</strong>
            </Typography>
          )}
          {error && <Typography className="error" sx={{ paddingTop: 4 }}>{error}</Typography>}
        </CardContent>
      </Card>
    </Container>
  );
}

export default App;
