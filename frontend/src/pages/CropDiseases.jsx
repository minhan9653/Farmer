import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

export default function CropDiseases() {
  const { cropId } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`/api/encyclopedia/crops/${cropId}/diseases`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => {});
  }, [cropId]);

  if (!data) return <div className="text-center py-20 text-gray-400">로딩 중...</div>;

  const diseases = data.diseases || [];
  const illnesses = diseases.filter((d) => d.category === "병");
  const pests = diseases.filter((d) => d.category === "해충");

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="mb-4">
        <Link to="/encyclopedia" className="text-green-700 hover:underline text-sm">← 도감 목록</Link>
      </div>
      <div className="bg-gradient-to-r from-gray-700 to-gray-900 text-white rounded-2xl p-10 mb-10 text-center">
        <h1 className="text-4xl font-extrabold">{data.crop.name}</h1>
        <p className="mt-2 opacity-80">병·해충</p>
      </div>

      {illnesses.length > 0 && (
        <>
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">— 병 —</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
            {illnesses.map((d) => (
              <Link key={d.id} to={`/encyclopedia/${cropId}/${d.id}`} className="group">
                <div className="bg-white rounded-xl shadow-md p-5 text-center hover:shadow-lg transition-shadow">
                  <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <span className="text-red-600 text-xl">🦠</span>
                  </div>
                  <h3 className="font-semibold text-gray-800 group-hover:text-green-700 transition-colors">
                    {d.name}
                  </h3>
                </div>
              </Link>
            ))}
          </div>
        </>
      )}

      {pests.length > 0 && (
        <>
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">— 해충 —</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {pests.map((d) => (
              <Link key={d.id} to={`/encyclopedia/${cropId}/${d.id}`} className="group">
                <div className="bg-white rounded-xl shadow-md p-5 text-center hover:shadow-lg transition-shadow">
                  <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <span className="text-orange-600 text-xl">🐛</span>
                  </div>
                  <h3 className="font-semibold text-gray-800 group-hover:text-green-700 transition-colors">
                    {d.name}
                  </h3>
                </div>
              </Link>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
