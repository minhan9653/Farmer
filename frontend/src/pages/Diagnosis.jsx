import { useState, useRef } from "react";

export default function Diagnosis() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileRef = useRef();

  const handleFile = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await fetch("/api/diagnosis/analyze", { method: "POST", body: formData });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch {
      setError("서버에 연결할 수 없습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-800 mb-2 text-center">🔬 AI 병해충 진단</h1>
      <p className="text-center text-gray-500 mb-8">농작물 사진을 업로드하면 AI가 병해충을 진단합니다</p>

      <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <div
          className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:border-green-500 transition-colors"
          onClick={() => fileRef.current.click()}
        >
          {preview ? (
            <img src={preview} alt="미리보기" className="max-h-64 mx-auto rounded-lg" />
          ) : (
            <div className="text-gray-400">
              <svg className="w-16 h-16 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p className="text-lg">클릭하여 이미지를 선택하세요</p>
              <p className="text-sm mt-1">JPG, PNG, WEBP 지원</p>
            </div>
          )}
          <input ref={fileRef} type="file" accept="image/*" onChange={handleFile} className="hidden" />
        </div>

        {file && (
          <div className="mt-4 flex items-center justify-between">
            <span className="text-sm text-gray-600">📎 {file.name}</span>
            <button
              type="submit"
              disabled={loading}
              className="bg-green-700 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-800 disabled:opacity-50 transition-colors"
            >
              {loading ? "분석 중..." : "진단 시작"}
            </button>
          </div>
        )}
      </form>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-8 text-red-700">{error}</div>
      )}

      {result && (
        <div className="space-y-8">
          {/* Annotated image */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📷 분석 결과 이미지</h2>
            <img
              src={`data:image/jpeg;base64,${result.image}`}
              alt="분석 결과"
              className="w-full rounded-lg"
            />
          </div>

          {/* Detections */}
          <div className="grid md:grid-cols-2 gap-4">
            {result.detections.map((det, i) => (
              <div key={i} className="bg-white rounded-xl shadow-md p-5">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-bold text-gray-800">{det.display_name}</h3>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      det.link ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"
                    }`}
                  >
                    {det.link ? "병해 감지" : "정상"}
                  </span>
                </div>
                <p className="text-gray-600 text-sm mb-3">{det.description}</p>
                <div className="mb-2">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>신뢰도</span>
                    <span>{det.confidence}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className={`h-2.5 rounded-full ${det.link ? "bg-red-500" : "bg-green-500"}`}
                      style={{ width: `${det.confidence}%` }}
                    />
                  </div>
                </div>
                {det.link && (
                  <a
                    href={det.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-green-700 text-sm font-medium hover:underline"
                  >
                    상세 정보 보기 →
                  </a>
                )}
              </div>
            ))}
          </div>

          {result.detections.length === 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 text-center text-yellow-700">
              탐지된 병해충이 없습니다. 다른 이미지를 시도해 보세요.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
