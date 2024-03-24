import React, { useState } from 'react';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleProcessImage = async () => {
    if (!image) {
      console.error("No image selected.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", image);
  
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });
  
    if (response.ok) {
      const data = await response.json();
      setProcessedImage(data.image);
    } else {
      console.error('Error processing image');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <nav>
          <ul>
            <li>Home</li>
            <li>About</li>
            <li>Contact</li>
          </ul>
        </nav>
      </header>
      <main>
        <section>
          <h2>Upload an image</h2>
          <input type="file" onChange={handleImageUpload} />
        </section>
        <section>
          <h2>Original image</h2>
          {image && <img src={image} alt="Original" />}
        </section>
        <section>
          <h2>Processed image</h2>
          {processedImage && <img src={processedImage} alt="Processed" />}
        </section>
        <button onClick={handleProcessImage}>Process image</button>
      </main>
    </div>
  );
}

export default App;