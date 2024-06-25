import React, { useState } from 'react';
import client from '../api/client'

const ImageForm: React.FC = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [response, setResponse] = useState<string | null>(null);
    const [file, setFile] = useState<Blob | string>('')

    const handleFileChange = (e: React.FormEvent<HTMLInputElement>) => {
        const { files } = e.target as unknown as { files: FileList }
        setFile(files[0])
    }

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        const form = new FormData()
        form.append('document_data', JSON.stringify({
            title,
            description
        }))
        form.append('image', file)

        try {
            const config = {
                headers: {
                    'content-type': 'multipart/form-data'
                }
            }

            const res = await client.post('/image-documents/', form, config);


            setResponse(res.data);
        } catch (error) {
            console.error('Error submitting the form:', error);
            setResponse('Error submitting the form');
        }

        setTitle('')
        setDescription('')
        //setFile('')
    };

    return (
        <div className="container">
            <h4>Create an Image Document</h4>
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

                <label htmlFor="image">Image</label>
                <input type="file" id="image" name="image" accept="image/png, image/jpeg" onChange={handleFileChange} />

                <button type="submit">Create Document</button>
            </form>
            {/* {response && <p>{response}</p>} */}
        </div>
    );
};

export default ImageForm;