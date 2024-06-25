import React from 'react';

const Home: React.FC = () => {
  return (   
    <div>
      <h2>AI Augmented Retrieval Demo</h2>
      <p>To get started, ensure the Backend API is running and see API docs at:</p> 
      <p> <a href={`${import.meta.env.VITE_BACKEND_API_BASE_URL}/docs`}>Backend OpenAPI Docs</a> </p>
      <p> For a primer on how this works, check out the <a href="/about"> About Page</a></p>
    </div>
  );
};

export default Home;