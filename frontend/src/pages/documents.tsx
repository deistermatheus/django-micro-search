import React from 'react';
import DocumentForm from '../components/DocumentForm';
import DocumentSearch from '../components/DocumentSearch';

const Documents: React.FC = () => {
  const [mode, setMode] = React.useState<String>('Search')
  
  const mapModeToComponent = (mode) => {
    if(mode === 'Search'){
      return <DocumentSearch/>
    } else if(mode === 'Create'){
      return <DocumentForm/>
    }
  }


  return (
    <div id="documents-home">
      <h3>Document Retrieval</h3>
      <select
        onChange={(e) => setMode(e.target.value)}
      >
        <option value="Search">Search</option>
        <option value="Create">Create</option>
      </select>
      {mapModeToComponent(mode)}
    </div>
  );
};

export default Documents;