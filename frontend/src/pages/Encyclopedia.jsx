import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function Encyclopedia() {
  const [crops, setCrops] = useState([]);

  useEffect(() => {
    fetch("/api/encyclopedia/crops")
      .then((r) => r.json())
      .then(setCrops)
      .catch(() => {});
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-800 mb-2 text-center">📖 도감 정보</h1>
      <p className="text-center text-gray-500 mb-10">작물을 선택하여 병해충 정보를 확인하세요</p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {crops.map((crop) => (
          <Link key={crop.id} to={`/encyclopedia/${crop.id}`} className="group">
            <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <img
                src={crop.image}
                alt={crop.name}
                className="w-full h-44 object-cover group-hover:scale-105 transition-transform duration-300"
              />
              <div className="p-4">
                <h3 className="text-lg font-semibold text-gray-800 group-hover:text-green-700 transition-colors">
                  {crop.name}
                </h3>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
