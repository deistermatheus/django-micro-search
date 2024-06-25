import React from 'react';
import ImageForm from '../components/ImageForm';
import ImageSearchForm from '../components/ImageSearchForm';

const Images: React.FC = () => {
  const [mode, setMode] = React.useState<String>('Search')
  
  const mapModeToComponent = (mode: String) => {
    if(mode === 'Search'){
      return <ImageSearchForm />
    } else if(mode === 'Create'){
      return <ImageForm/>
    }
  }

  return (
     <div id="images-home">
      <h3>Image Document Retrieval</h3>
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

export default Images;