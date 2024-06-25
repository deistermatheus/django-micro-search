import React, { useState } from 'react';
import client from '../api/client'

type SearchResult = {
    uuid: string
    description: string
    title: string
    distance: string
    image: string
}

type SearchResponse = {
    similar: SearchResult[]
    reasoning: string
}

const ImageSearchForm: React.FC = () => {
    const [prompt, setPrompt] = useState<string>('');
    const [file, setFile] = useState<Blob | string>('')
    const [response, setResponse] = useState<SearchResponse | null>(null);

    const handleFileChange = (e: React.FormEvent<HTMLInputElement>) => {
        const { files } = e.target as unknown as { files: FileList }
        setFile(files[0])
    }

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        const form = new FormData()

        form.append('query_options', JSON.stringify({
            analyze_results: Boolean(prompt),
            user_prompt: prompt
        }))

        form.append('image', file)

        try {
            const config = {
                headers: {
                    'content-type': 'multipart/form-data'
                }
            }

            const res = await client.post('/image-documents/search/', form, config);


            setResponse(res.data);
        } catch (error) {
            console.error('Error submitting the form:', error);
            setResponse(null);
        }

        setPrompt('')
    };

    const searchResults = (results: SearchResult[]) => {
        return (
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Score/Rank</th>
                        <th>Image Preview</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((result, index) => (
                        <tr key={result.uuid}>
                            <td>{result.title}</td>
                            <td>{result.description}</td>
                            <td>{result.distance ?? result.distance}</td>
                            <td><img width="50" height="50" src={result.image} onClick={() => window.open(result.image)}></img></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div className="container">
            <h4>Search Images</h4>
            <form onSubmit={handleSubmit}>

                <label htmlFor="user prompt">Optional GPT Prompt To Analyze results</label>
                <textarea
                    id="user prompt"
                    name="user prompt"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                ></textarea>

                <label htmlFor="image">Image</label>
                <input type="file" id="image" name="image" accept="image/png, image/jpeg" onChange={handleFileChange} />

                <button type="submit">Search Similar Images</button>
            </form>
            {response && <p>{response?.reasoning}</p>}
            {response && searchResults(response.similar)}
        </div>
    );
};

export default ImageSearchForm;