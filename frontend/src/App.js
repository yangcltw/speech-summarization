   import { useState } from "react";
   import FileUpload from "./components/FileUpload";
   import SummaryDisplay from "./components/SummaryDisplay";
   import Navbar from "./components/Navbar";
   import Loader from "./components/Loader";
   
   const App = () => {
       const [summary, setSummary] = useState("");
       const [loading, setLoading] = useState(false);
       
       const handleUploadSuccess = (data) => {
           setLoading(false);
           setSummary(data.summary);
       };
       
       return (
           <div>
               <Navbar />
               <FileUpload onUploadSuccess={handleUploadSuccess} />
               {loading ? <Loader /> : <SummaryDisplay summary={summary} />}
           </div>
       );
   };
   
   export default App;