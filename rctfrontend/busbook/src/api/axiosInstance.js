// src/api/axiosInstance.js
import axios from 'axios';
import { API_BASE_URL } from './const';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
