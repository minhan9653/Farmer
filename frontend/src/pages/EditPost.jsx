import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";

export default function EditPost() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({ title: "", content: "", password: "" });
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`/api/board/posts/${id}`)
      .then((r) => r.json())
      .then((data) => setForm({ title: data.title, content: data.content, password: "" }))
      .catch(() => {});
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    Object.entries(form).forEach(([k, v]) => formData.append(k, v));
    if (file) formData.append("image", file);

    const res = await fetch(`/api/board/posts/${id}`, { method: "PUT", body: formData });
    const data = await res.json();
    if (data.success) {
      navigate(`/board/${id}`);
    } else {
      setError(data.error || "수정 실패");
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <Link to={`/board/${id}`} className="text-green-700 hover:underline text-sm">← 돌아가기</Link>
      <h1 className="text-3xl font-bold text-gray-800 mt-4 mb-8">📝 글 수정</h1>

      {error && <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6 text-red-700">{error}</div>}

      <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-8 space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">제목</label>
          <input
            type="text"
            required
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">내용</label>
          <textarea
            required
            rows={8}
            value={form.content}
            onChange={(e) => setForm({ ...form, content: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none resize-y"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">비밀번호</label>
          <input
            type="password"
            required
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            placeholder="게시물 작성 시 설정한 비밀번호"
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">이미지 변경 (선택)</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-green-50 file:text-green-700 file:font-medium hover:file:bg-green-100"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-yellow-500 text-white py-3 rounded-lg font-semibold hover:bg-yellow-600 transition-colors"
        >
          수정하기
        </button>
      </form>
    </div>
  );
}
