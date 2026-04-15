import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";

export default function Board() {
  const [posts, setPosts] = useState([]);
  const [search, setSearch] = useState("");
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const q = searchParams.get("q");
    const url = q ? `/api/board/posts/search?q=${encodeURIComponent(q)}` : "/api/board/posts";
    fetch(url)
      .then((r) => r.json())
      .then(setPosts)
      .catch(() => {});
  }, [searchParams]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (search.trim()) {
      window.location.href = `/board?q=${encodeURIComponent(search)}`;
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">📋 게시판</h1>

      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <form onSubmit={handleSearch} className="flex-1 flex gap-2">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="검색어 입력..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
          />
          <button type="submit" className="bg-green-700 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-800 transition-colors">
            검색
          </button>
        </form>
        <Link
          to="/board/create"
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors text-center"
        >
          ✏️ 글쓰기
        </Link>
      </div>

      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr className="text-left text-sm text-gray-500">
              <th className="px-6 py-3 w-12">#</th>
              <th className="px-6 py-3">제목</th>
              <th className="px-6 py-3 w-24 hidden sm:table-cell">작성자</th>
              <th className="px-6 py-3 w-16 hidden sm:table-cell">조회</th>
              <th className="px-6 py-3 w-28 hidden md:table-cell">날짜</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {posts.map((post) => (
              <tr key={post.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 text-sm text-gray-400">{post.id}</td>
                <td className="px-6 py-4">
                  <Link to={`/board/${post.id}`} className="text-gray-800 font-medium hover:text-green-700 transition-colors">
                    {post.title}
                    {post.comment_count > 0 && (
                      <span className="ml-2 text-xs text-green-600">[{post.comment_count}]</span>
                    )}
                  </Link>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 hidden sm:table-cell">{post.author}</td>
                <td className="px-6 py-4 text-sm text-gray-400 hidden sm:table-cell">{post.views}</td>
                <td className="px-6 py-4 text-xs text-gray-400 hidden md:table-cell">
                  {post.created_at ? new Date(post.created_at).toLocaleDateString("ko-KR") : ""}
                </td>
              </tr>
            ))}
            {posts.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-gray-400">
                  게시물이 없습니다.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
