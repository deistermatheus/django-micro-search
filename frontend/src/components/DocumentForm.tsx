import React, { useState } from 'react';
import client from '../api/client'

const DocumentForm: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [response, setResponse] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const res = await client.post('/documents/', {
        title,
        description,
      });
      console.log(response)
      setResponse(res.data.message);
    } catch (error) {
      console.error('Error submitting the form:', error);
      setResponse('Error submitting the form');
    }

    setTitle('')
    setDescription('')
  };

  return (
    <div className="container">
      <h4>Create a Document</h4>
      <form onSubmit={handleSubmit}>
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>

        <button type="submit">Create Document</button>
      </form>
      {response && <p>{response}</p>}
    </div>
  );
};

export default DocumentForm;