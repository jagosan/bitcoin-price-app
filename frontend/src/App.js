import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Container, Paper, Typography, Box } from '@mui/material';

function App() {
  const [priceData, setPriceData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/bitcoin/price');
        if (response.data.success) {
          const formattedData = response.data.data.map(item => ({
            date: new Date(item.timestamp).toLocaleDateString(),
            price: item.price
          }));
          setPriceData(formattedData);
        } else {
          setError('Failed to fetch Bitcoin price data');
        }
      } catch (err) {
        setError('Error connecting to the server');
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 300000); // Refresh every 5 minutes
    return () => clearInterval(interval);
  }, []);

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Bitcoin Price Chart
        </Typography>
        <Paper elevation={3} sx={{ p: 3 }}>
          {error ? (
            <Typography color="error" align="center">{error}</Typography>
          ) : (
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={priceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis 
                  domain={['auto', 'auto']}
                  label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke="#8884d8" 
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </Paper>
      </Box>
    </Container>
  );
}

export default App; 