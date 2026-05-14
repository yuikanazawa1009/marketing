'use client'

import React, { useState } from 'react'
import { ChevronDown, Mail, Phone, Instagram } from 'lucide-react'

interface StaffMember {
  id: string
  name: string
  role: string
  emoji: string
  color: string
  bio?: string
  achievements: string[]
  works: { title: string; url: string }[]
  contact?: {
    phone?: string
    email?: string
    instagram?: string
    tiktok?: string
  }
}

export default function RoyalMatchStaff() {
  const [expanded, setExpanded] = useState<string | null>(null)

  const staff = [
    {
      id: 'saco',
      name: 'Saco Makita',
      role: 'Lead Choreographer',
      emoji: '👩‍🎤',
      color: 'red',
      bio: 'Born: Nov 10, 1993 | Height: 161cm',
      achievements: [
        '16M+ views on FRUITS ZIPPER (NEW KAWAII)',
        'Multi-platform viral choreographer',
        'Regular TV appearance: ZIP! SHOWBIZ, THE RULES'
      ],
      works: [
        { title: 'FRUITS ZIPPER - NEW KAWAII', url: 'https://tiktok.com/@saco_makita' },
        { title: 'KAWAII LAB. Series (4 titles)', url: 'https://instagram.com/sacomakita' },
        { title: 'CUTIE STREET Choreography', url: 'https://tiktok.com/@saco_makita' }
      ],
      contact: {
        phone: '070-2296-9590',
        email: 'mine@focpro.co.jp',
        instagram: 'sacomakita',
        tiktok: 'saco_makita'
      }
    },
    {
      id: 'director',
      name: 'Nao Watanabe',
      role: 'Creative Director',
      emoji: '🎬',
      color: 'blue',
      bio: 'Born: February 1985 | GLASSLOFT Inc.',
      achievements: [
        '61st ACC TOKYO CREATIVITY AWARDS Winner (2021)',
        '58th ACC TOKYO CREATIVITY AWARDS Winner (2018)',
        'Foorin "Paprika" MV & 100+ Commercial Works'
      ],
      works: [
        { title: 'NISSIN Campaign - Director', url: 'https://youtube.com/results?search_query=NISSIN+CM' },
        { title: 'GU Brand Work Collection', url: 'https://youtube.com/results?search_query=GU+CM' },
        { title: 'UCC & CAPCOM Campaigns', url: 'https://youtube.com/results?search_query=UCC+CAPCOM+CM' }
      ],
      contact: {
        email: 'contact@glassloft.jp'
      }
    },
    {
      id: 'producer',
      name: 'Yuki Suzuki',
      role: 'Producer & Project Lead',
      emoji: '📋',
      color: 'purple',
      achievements: [
        '100+ Projects Delivered',
        'Schedule & Budget Master',
        'Team Coordination Expert'
      ],
      works: [
        { title: 'Royal Match TVCM Series', url: 'https://youtube.com/watch?v=example3' },
        { title: 'Behind the Scenes Coordination', url: 'https://youtube.com/watch?v=example4' }
      ]
    },
    {
      id: 'editor',
      name: 'Haruto Tanaka',
      role: 'Video Editor & VFX',
      emoji: '✂️',
      color: 'pink',
      achievements: [
        'Emmy-nominated editing',
        'Motion Graphics Master',
        '200+ Commercial Edits'
      ],
      works: [
        { title: 'Royal Match - Dynamic Edit Version', url: 'https://youtube.com/watch?v=example5' },
        { title: 'VFX Showcase Reel', url: 'https://youtube.com/watch?v=example6' }
      ]
    },
    {
      id: 'sound',
      name: 'Tetsu Midorikawa',
      role: 'Sound Director & Music Producer',
      emoji: '🎵',
      color: 'green',
      bio: 'Born: 1972 | Fukuoka | Founded Melody Punch Inc. (2005)',
      achievements: [
        'CM Music Specialist since 1996',
        '30+ Major Brand Campaigns (au, SoftBank, KIRIN, etc.)',
        'Founder & Producer at Melody Punch Inc.'
      ],
      works: [
        { title: 'Major Brand Campaign Music', url: 'http://melodypunch.co.jp/' },
        { title: 'Drama & Film Scoring', url: 'http://melodypunch.co.jp/works_tag/midorikawa' },
        { title: 'Commercial Music Portfolio', url: 'http://melodypunch.co.jp/works_tag/midorikawa' }
      ],
      contact: {
        email: 'contact@melodypunch.co.jp'
      }
    },
    {
      id: 'art',
      name: 'Kenji Nakamura',
      role: 'Art Director & Set Design',
      emoji: '🎨',
      color: 'yellow',
      achievements: [
        'Tokyo Design Award Winner',
        'Minimalist Aesthetics Pioneer',
        '75+ Commercial Sets'
      ],
      works: [
        { title: 'Royal Match Visual Identity', url: 'https://youtube.com/watch?v=example9' },
        { title: 'Studio Setup Design', url: 'https://youtube.com/watch?v=example10' }
      ]
    },
    {
      id: 'casting',
      name: 'Mika Kobayashi',
      role: 'Casting Director',
      emoji: '⭐',
      color: 'orange',
      achievements: [
        'Celebrity Network Expert',
        'Talent Matching Specialist',
        'International Casting Connections'
      ],
      works: [
        { title: 'Royal Match Talent Selection', url: 'https://youtube.com/watch?v=example11' },
        { title: 'Talent Database & Profiles', url: 'https://youtube.com/watch?v=example12' }
      ]
    },
    {
      id: 'camera',
      name: 'Riku Fujita',
      role: 'Director of Photography',
      emoji: '📹',
      color: 'indigo',
      achievements: [
        'Cinematography Master',
        'Multi-camera Specialist',
        '30+ Awards for Visual Excellence'
      ],
      works: [
        { title: 'Royal Match Cinematography Reel', url: 'https://youtube.com/watch?v=example13' },
        { title: 'Color Grading Showcase', url: 'https://youtube.com/watch?v=example14' }
      ]
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* ヘッダー */}
      <header className="bg-gradient-to-r from-amber-400 to-yellow-300 p-8 shadow-lg">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold text-black mb-2">🎬 ROYAL MATCH</h1>
          <p className="text-lg text-gray-800">TVCM製作 ─ 制作チーム紹介</p>
        </div>
      </header>

      {/* メインコンテンツ */}
      <div className="max-w-6xl mx-auto p-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-2">制作チーム</h2>
          <p className="text-gray-600">Royal Matchの世界を創造するプロフェッショナルたちをご紹介</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {staff.map((s) => (
            <div
              key={s.id}
              className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
            >
              {/* 写真エリア */}
              <div className={`bg-gradient-to-br h-48 flex items-center justify-center text-7xl ${
                s.color === 'red' ? 'from-pink-100 to-rose-100' :
                s.color === 'blue' ? 'from-blue-100 to-cyan-100' :
                s.color === 'purple' ? 'from-purple-100 to-pink-100' :
                s.color === 'pink' ? 'from-pink-100 to-rose-100' :
                s.color === 'green' ? 'from-green-100 to-emerald-100' :
                s.color === 'yellow' ? 'from-yellow-100 to-amber-100' :
                s.color === 'orange' ? 'from-orange-100 to-yellow-100' :
                'from-indigo-100 to-blue-100'
              }`}>
                {s.emoji}
              </div>

              {/* 情報 */}
              <div className="p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-1">{s.name}</h3>
                <p className="text-gray-600 text-sm font-semibold mb-1">{s.role}</p>
                {s.bio && <p className="text-gray-500 text-xs mb-4">{s.bio}</p>}

                <button
                  onClick={() => setExpanded(expanded === s.id ? null : s.id)}
                  className={`w-full py-2 px-4 rounded-lg font-semibold transition flex justify-between items-center ${
                    s.color === 'red' ? 'bg-red-50 text-red-600 hover:bg-red-100' :
                    s.color === 'blue' ? 'bg-blue-50 text-blue-600 hover:bg-blue-100' :
                    s.color === 'purple' ? 'bg-purple-50 text-purple-600 hover:bg-purple-100' :
                    s.color === 'pink' ? 'bg-pink-50 text-pink-600 hover:bg-pink-100' :
                    s.color === 'green' ? 'bg-green-50 text-green-600 hover:bg-green-100' :
                    s.color === 'yellow' ? 'bg-yellow-50 text-yellow-600 hover:bg-yellow-100' :
                    s.color === 'orange' ? 'bg-orange-50 text-orange-600 hover:bg-orange-100' :
                    'bg-indigo-50 text-indigo-600 hover:bg-indigo-100'
                  }`}
                >
                  詳細を見る
                  <ChevronDown size={20} className={`transition-transform ${expanded === s.id ? 'rotate-180' : ''}`} />
                </button>

                {expanded === s.id && (
                  <div className="mt-4 space-y-4 border-t pt-4">
                    <div>
                      <h4 className="font-bold text-gray-700 text-sm mb-2 uppercase">実績</h4>
                      <ul className="space-y-1">
                        {s.achievements.map((a, i) => (
                          <li key={i} className="text-gray-600 text-sm">✓ {a}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-bold text-gray-700 text-sm mb-2 uppercase">作品</h4>
                      <div className="space-y-1">
                        {s.works.map((w, i) => (
                          <a
                            key={i}
                            href={w.url}
                            target="_blank"
                            className={`block text-sm font-semibold hover:underline ${
                              s.color === 'red' ? 'text-red-600' :
                              s.color === 'blue' ? 'text-blue-600' :
                              s.color === 'purple' ? 'text-purple-600' :
                              s.color === 'pink' ? 'text-pink-600' :
                              s.color === 'green' ? 'text-green-600' :
                              s.color === 'yellow' ? 'text-yellow-600' :
                              s.color === 'orange' ? 'text-orange-600' :
                              'text-indigo-600'
                            }`}
                          >
                            ▶ {w.title}
                          </a>
                        ))}
                      </div>
                    </div>
                    {s.contact && (
                      <div className="border-t pt-3">
                        <h4 className="font-bold text-gray-700 text-sm mb-2 uppercase">連絡先</h4>
                        <div className="space-y-2 text-sm">
                          {s.contact.phone && (
                            <div className="flex items-center gap-2 text-gray-600">
                              <Phone size={14} />
                              <span>{s.contact.phone}</span>
                            </div>
                          )}
                          {s.contact.email && (
                            <div className="flex items-center gap-2">
                              <Mail size={14} />
                              <a href={`mailto:${s.contact.email}`} className="text-blue-600 hover:underline">
                                {s.contact.email}
                              </a>
                            </div>
                          )}
                          {(s.contact.instagram || s.contact.tiktok) && (
                            <div className="flex items-center gap-2 text-gray-600">
                              <Instagram size={14} />
                              <div className="flex gap-2">
                                {s.contact.instagram && (
                                  <a href={`https://instagram.com/${s.contact.instagram}`} target="_blank" className="text-blue-600 hover:underline">
                                    @{s.contact.instagram}
                                  </a>
                                )}
                                {s.contact.tiktok && (
                                  <a href={`https://tiktok.com/@${s.contact.tiktok}`} target="_blank" className="text-blue-600 hover:underline">
                                    TikTok
                                  </a>
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* フッター */}
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="max-w-6xl mx-auto px-8 text-center">
          <p className="text-sm">© 2024 Royal Match TVCM Production. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
