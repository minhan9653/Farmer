import { Link, NavLink } from "react-router-dom";
import { useState } from "react";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  const linkClass = ({ isActive }) =>
    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      isActive
        ? "bg-green-700 text-white"
        : "text-green-100 hover:bg-green-600 hover:text-white"
    }`;

  return (
    <nav className="bg-green-800 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl">🌱</span>
            <span className="text-white text-xl font-bold">FARMER</span>
          </Link>

          {/* Desktop */}
          <div className="hidden md:flex items-center space-x-1">
            <NavLink to="/" end className={linkClass}>홈</NavLink>
            <NavLink to="/diagnosis" className={linkClass}>AI 진단</NavLink>
            <NavLink to="/encyclopedia" className={linkClass}>도감 정보</NavLink>
            <NavLink to="/board" className={linkClass}>게시판</NavLink>
          </div>

          {/* Mobile toggle */}
          <button
            onClick={() => setOpen(!open)}
            className="md:hidden text-green-100 hover:text-white focus:outline-none"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {open ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden px-4 pb-3 space-y-1">
          <NavLink to="/" end className={linkClass} onClick={() => setOpen(false)}>홈</NavLink>
          <NavLink to="/diagnosis" className={linkClass} onClick={() => setOpen(false)}>AI 진단</NavLink>
          <NavLink to="/encyclopedia" className={linkClass} onClick={() => setOpen(false)}>도감 정보</NavLink>
          <NavLink to="/board" className={linkClass} onClick={() => setOpen(false)}>게시판</NavLink>
        </div>
      )}
    </nav>
  );
}
