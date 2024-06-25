import React, { useState } from 'react';
import client from '../api/client'


type SearchResult = {
    uuid: string
    description: string
    title: string
    rank: string | null
    distance: string | null
    image: string
}

const DocumentSearch: React.FC = () => {
    const [query, setQuery] = useState('');
    const [mode, setMode] = useState('semantic');
    const [response, setResponse] = useState<SearchResult[] | null>(null);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();

        try {
            const res = await client.get('/documents/search/', {
                params: {
                    q: query,
                    mode
                }
            });

            setResponse(res.data);
        } catch (error) {
            console.error('Error submitting the form:', error);
            setResponse(null);
        }
    };

    const searchResults = (results: SearchResult[]) => {
        return (
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Score/Rank</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((result, index) => (
                        <tr key={result.uuid}>
                            <td>{result.title}</td>
                            <td>{result.description}</td>
                            <td>{result.distance ? result.distance : result.rank}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div className="search-container">
            <div className='search-form'>
                <h4>Search your Documents </h4>
                {
                    <form onSubmit={handleSubmit}>
                        <label htmlFor="query">Query</label>
                        <input
                            type="text"
                            id="query"
                            name="query"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />

                        <label htmlFor="Query Mode">Query Mode</label>
                        <select
                            id="mode"
                            name="mode"
                            onChange={(e) => setMode(e.target.value)}

                        >
                            <option value="semantic">Semantic</option>
                            <option value="textual">Text</option>
                            <option value="hybrid">Hybrid</option>
                        </select>
                        <button type="submit">Submit Query</button>
                    </form>
                }
            </div>
            <div className="search-results">
                <h3>Search Results</h3>
                <p>
                    {
                        response && searchResults(response)
                    }
                </p>
            </div>
        </div>
    );
};

export default DocumentSearch;