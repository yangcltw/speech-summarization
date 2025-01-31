import axios from "axios";

export const uploadAudio = async (file) => {
    try {
        const formData = new FormData();
        formData.append("file", file);
        const response = await axios.post("http://localhost:8002/process/", formData, {
            headers: { "Content-Type": "multipart/form-data"},});
        console.log("api.js Response:", response.data);
        return response.data;
    } catch (error) {
        console.error("Upload failed:", error);
    }
};