import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

export default function DiseaseDetail() {
  const { cropId, diseaseId } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`/api/encyclopedia/diseases/${diseaseId}`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => {});
  }, [diseaseId]);

  if (!data) return <div className="text-center py-20 text-gray-400">로딩 중...</div>;

  const { disease, crop } = data;

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <div className="mb-4">
        <Link to={`/encyclopedia/${cropId}`} className="text-green-700 hover:underline text-sm">
          ← {crop.name} 목록
        </Link>
      </div>

      <div className="bg-gradient-to-r from-gray-700 to-gray-900 text-white rounded-2xl p-10 mb-8 text-center">
        <h1 className="text-3xl font-extrabold">{disease.name}</h1>
        <p className="mt-2 opacity-80">{crop.name} · {disease.category}</p>
      </div>

      <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div className="border-b p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            <span className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-sm">🌤</span>
            발생환경
          </h2>
          <p className="text-gray-600 leading-relaxed">{disease.environment}</p>
        </div>
        <div className="border-b p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            <span className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center text-sm">🔍</span>
            증상설명
          </h2>
          <p className="text-gray-600 leading-relaxed">{disease.symptoms}</p>
        </div>
        <div className="p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            <span className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-sm">💊</span>
            방제방법
          </h2>
          <p className="text-gray-600 leading-relaxed">{disease.treatment}</p>
        </div>
      </div>
    </div>
  );
}
