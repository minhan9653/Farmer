import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Diagnosis from "./pages/Diagnosis";
import Encyclopedia from "./pages/Encyclopedia";
import CropDiseases from "./pages/CropDiseases";
import DiseaseDetail from "./pages/DiseaseDetail";
import Board from "./pages/Board";
import PostDetail from "./pages/PostDetail";
import CreatePost from "./pages/CreatePost";
import EditPost from "./pages/EditPost";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/diagnosis" element={<Diagnosis />} />
          <Route path="/encyclopedia" element={<Encyclopedia />} />
          <Route path="/encyclopedia/:cropId" element={<CropDiseases />} />
          <Route path="/encyclopedia/:cropId/:diseaseId" element={<DiseaseDetail />} />
          <Route path="/board" element={<Board />} />
          <Route path="/board/create" element={<CreatePost />} />
          <Route path="/board/:id" element={<PostDetail />} />
          <Route path="/board/:id/edit" element={<EditPost />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
