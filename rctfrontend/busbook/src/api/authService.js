// src/authService.js
import axiosInstance from "./axiosInstance";

axiosInstance.interceptors.request.use(
  (config) => {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
      config.headers.Authorization = `Bearer ${access_token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response.status === 401 && originalRequest._retry) {
        console.log("Inside Intercept 3", originalRequest, error)
      originalRequest._retry = true;
      const refresh_token = localStorage.getItem("refresh_token");

      try {
        const data = await renewToken(refresh_token);
        
        localStorage.setItem("access_token", data.token);

        axiosInstance.defaults.headers[
          "Authorization"
        ] = `Bearer ${data.token}`;
        return axiosInstance(originalRequest);
      } catch (err) {
        console.error("Token renewal failed", err);
      }
    }

    return Promise.reject(error);
  }
);

export const login = async (username, password) => {
  let success = false;
  await axiosInstance
    .post("/token/", {
      username,
      password,
    })
    .then((resp) => {
      localStorage.setItem("access_token", resp.data.access_token);
      localStorage.setItem("refresh_token", resp.data.refresh_token);
      success = true;
    })
    .catch(() => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    });

  return success;
};

export const renewToken = async (longLivedToken) => {
  const response = await axiosInstance.put("/token/", {
    token: longLivedToken,
  });
  return response.data;
};
