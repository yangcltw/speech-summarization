 // FileUpload.js
import { useState } from "react";
import { uploadAudio } from "../services/api";

const FileUpload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);

    const handleUpload = async () => {
        if (file) {
            const response = await uploadAudio(file);
            onUploadSuccess(response);
        }
    };
    return (
        <div>
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <button onClick={handleUpload}>Upload</button>
        </div>
    );
};

export default FileUpload;