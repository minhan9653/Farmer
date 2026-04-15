import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";

export default function PostDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [comment, setComment] = useState("");
  const [deleteModal, setDeleteModal] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const loadPost = () => {
    fetch(`/api/board/posts/${id}`)
      .then((r) => r.json())
      .then(setPost)
      .catch(() => {});
  };

  useEffect(loadPost, [id]);

  const handleComment = async (e) => {
    e.preventDefault();
    if (!comment.trim()) return;
    await fetch(`/api/board/posts/${id}/comments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: comment }),
    });
    setComment("");
    loadPost();
  };

  const handleDeleteComment = async (commentId) => {
    await fetch(`/api/board/comments/${commentId}`, { method: "DELETE" });
    loadPost();
  };

  const handleDelete = async () => {
    const res = await fetch(`/api/board/posts/${id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    const data = await res.json();
    if (data.success) {
      navigate("/board");
    } else {
      setError(data.error || "삭제 실패");
    }
  };

  if (!post) return <div className="text-center py-20 text-gray-400">로딩 중...</div>;

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <Link to="/board" className="text-green-700 hover:underline text-sm">← 목록으로</Link>

      <article className="bg-white rounded-2xl shadow-lg mt-4 overflow-hidden">
        <div className="p-8">
          <h1 className="text-2xl font-bold text-gray-800 mb-3">{post.title}</h1>
          <div className="flex items-center gap-4 text-sm text-gray-500 mb-6">
            <span>👤 {post.author}</span>
            <span>👁 {post.views}</span>
            <span>{post.created_at ? new Date(post.created_at).toLocaleDateString("ko-KR") : ""}</span>
          </div>

          {post.image && (
            <img src={`/uploads/${post.image}`} alt="첨부 이미지" className="rounded-lg mb-6 max-w-full" />
          )}

          <div className="prose text-gray-700 whitespace-pre-wrap">{post.content}</div>
        </div>

        <div className="border-t px-8 py-4 flex gap-3 bg-gray-50">
          <Link
            to={`/board/${id}/edit`}
            className="bg-yellow-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-yellow-600 transition-colors"
          >
            수정
          </Link>
          <button
            onClick={() => setDeleteModal(true)}
            className="bg-red-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-600 transition-colors"
          >
            삭제
          </button>
        </div>
      </article>

      {/* Comments */}
      <section className="mt-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">💬 댓글 ({post.comments?.length || 0})</h2>
        <div className="space-y-3 mb-6">
          {(post.comments || []).map((c) => (
            <div key={c.id} className="bg-white rounded-lg shadow-sm p-4 flex justify-between items-start">
              <div>
                <p className="text-gray-700">{c.text}</p>
                <span className="text-xs text-gray-400 mt-1 block">
                  {c.created_at ? new Date(c.created_at).toLocaleDateString("ko-KR") : ""}
                </span>
              </div>
              <button
                onClick={() => handleDeleteComment(c.id)}
                className="text-red-400 hover:text-red-600 text-sm ml-4"
              >
                삭제
              </button>
            </div>
          ))}
        </div>

        <form onSubmit={handleComment} className="flex gap-2">
          <input
            type="text"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="댓글을 입력하세요..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
          />
          <button type="submit" className="bg-green-700 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-800 transition-colors">
            등록
          </button>
        </form>
      </section>

      {/* Delete Modal */}
      {deleteModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setDeleteModal(false)}>
          <div className="bg-white rounded-2xl p-8 w-full max-w-sm mx-4" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-bold text-gray-800 mb-4">게시물 삭제</h3>
            <p className="text-gray-600 mb-4">비밀번호를 입력하세요.</p>
            {error && <p className="text-red-500 text-sm mb-3">{error}</p>}
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="비밀번호"
              className="w-full border border-gray-300 rounded-lg px-4 py-2 mb-4 focus:ring-2 focus:ring-red-500 outline-none"
            />
            <div className="flex gap-3">
              <button
                onClick={() => setDeleteModal(false)}
                className="flex-1 border border-gray-300 py-2 rounded-lg font-medium hover:bg-gray-50"
              >
                취소
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 bg-red-500 text-white py-2 rounded-lg font-medium hover:bg-red-600"
              >
                삭제
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
