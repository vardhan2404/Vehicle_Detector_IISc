import React, { useState } from 'react';
import axios from 'axios';

const ImageUploader = () => {
  const [image, setImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('image', image);

    try {
      const response = await axios.post('/process', formData);
      setProcessedImage(response.data.processedImage);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <nav>
        <ul>
          <li>Home</li>
          <li>About</li>
          <li>Contact</li>
        </ul>
      </nav>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleImageChange} />
        <button type="submit">Upload</button>
      </form>
      <div>
        <h2>Original Image</h2>
        {image && <img src={URL.createObjectURL(image)} alt="Original" />}
      </div>
      <div>
        <h2>Processed Image</h2>
        {processedImage && <img src={processedImage} alt="Processed" />}
      </div>
    </div>
  );
};

export default ImageUploader;