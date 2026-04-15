import { Link } from "react-router-dom";

const TEAM = [
  { num: "01", name: "박경호" },
  { num: "02", name: "신재호" },
  { num: "03", name: "김민한" },
  { num: "04", name: "이건창" },
];

const CROPS = [
  { name: "가지", img: "https://images.unsplash.com/photo-1613743983303-b3e89f8a2b80?w=400" },
  { name: "토마토", img: "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=400" },
  { name: "상추", img: "https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=400" },
  { name: "배추", img: "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400" },
  { name: "당근", img: "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400" },
  { name: "무", img: "https://images.unsplash.com/photo-1585500671198-63e978bca498?w=400" },
  { name: "딸기", img: "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400" },
  { name: "고추", img: "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=400" },
];

const LINKS = [
  { name: "농사로", url: "https://www.nongsaro.go.kr/portal/portalMain.ps?menuId=PS00001" },
  { name: "농업기술", url: "https://www.nongsaro.go.kr/portal/ps/psb/psbx/cropEbookMain.ps?menuId=PS65290" },
  { name: "주간농사정보", url: "https://www.nongsaro.go.kr/portal/ps/psz/psza/contentMain.ps?menuId=PS00199" },
  { name: "작목정보", url: "https://www.nongsaro.go.kr/portal/farmTechMain.ps?menuId=PS65291&stdPrdlstCode=FC050501" },
  { name: "농업기술동영상", url: "http://www.nongsaro.go.kr/portal/ps/psb/psbo/farmngTchnlgyMvpLst.ps?menuId=PS00069&pageUnit=9" },
  { name: "농약검색", url: "https://psis.rda.go.kr/psis/agc/res/agchmRegistStusLst.ps?menuId=PS00263" },
];

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <section className="relative bg-gradient-to-br from-green-700 to-green-900 text-white py-24 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-4 tracking-tight">FARMER</h1>
          <p className="text-xl md:text-2xl font-light opacity-90">농작물 병해충 AI 진단 서비스</p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link
              to="/diagnosis"
              className="bg-white text-green-800 px-8 py-3 rounded-full font-semibold hover:bg-green-50 transition-colors shadow-lg"
            >
              🔍 AI 진단 시작
            </Link>
            <Link
              to="/encyclopedia"
              className="border-2 border-white px-8 py-3 rounded-full font-semibold hover:bg-white/10 transition-colors"
            >
              📖 도감 보기
            </Link>
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-16 px-4 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-2">FARMER</h2>
        <p className="text-center text-gray-500 mb-10">팀원</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {TEAM.map((m) => (
            <div key={m.num} className="bg-white rounded-xl shadow-md p-6 text-center hover:shadow-lg transition-shadow">
              <span className="text-green-600 font-bold text-sm">{m.num}</span>
              <h3 className="text-lg font-semibold mt-2 text-gray-800">{m.name}</h3>
            </div>
          ))}
        </div>
      </section>

      {/* Diagnosis CTA */}
      <section className="bg-green-50 py-16 px-4">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl font-bold text-gray-800 mb-2">병해충 진단 프로그램</h2>
            <p className="text-gray-500 mb-4">이미지를 업로드 해보세요</p>
            <p className="text-gray-600">AI가 농작물 사진을 분석하여 병해충을 진단해드립니다.</p>
          </div>
          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              to="/diagnosis"
              className="flex-1 bg-green-700 text-white text-center py-4 rounded-lg font-semibold hover:bg-green-800 transition-colors shadow"
            >
              🔬 AI 진단하기
            </Link>
            <Link
              to="/board"
              className="flex-1 bg-gray-600 text-white text-center py-4 rounded-lg font-semibold hover:bg-gray-700 transition-colors shadow"
            >
              📋 게시판
            </Link>
          </div>
        </div>
      </section>

      {/* Crops */}
      <section className="py-16 px-4 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-2">도감 정보</h2>
        <p className="text-center text-gray-500 mb-10">다양한 작물들을 확인해 보세요</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {CROPS.map((crop) => (
            <Link key={crop.name} to="/encyclopedia" className="group">
              <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <img src={crop.img} alt={crop.name} className="w-full h-40 object-cover group-hover:scale-105 transition-transform duration-300" />
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-gray-800">{crop.name}</h3>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Farm Links */}
      <section className="bg-gray-100 py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-2">농사로</h2>
          <p className="text-center text-gray-500 mb-10">자주 찾는 항목들</p>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {LINKS.map((link) => (
              <a
                key={link.name}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-white p-6 rounded-xl shadow-md text-center font-semibold text-gray-700 hover:text-green-700 hover:shadow-lg transition-all"
              >
                {link.name} →
              </a>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
