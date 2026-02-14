'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const links = [
  { href: '/', label: 'Inicio' },
  { href: '/tournaments', label: 'Torneos' },
  { href: '/fields', label: 'Canchas' },
  { href: '/referees', label: 'Árbitros' },
]

export default function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="bg-emerald-700 text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-2xl font-bold tracking-tight">
            TuLiga
          </Link>
          <div className="flex gap-1">
            {links.map(link => {
              const active = pathname === link.href
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    active
                      ? 'bg-emerald-900 text-white'
                      : 'text-emerald-100 hover:bg-emerald-600'
                  }`}
                >
                  {link.label}
                </Link>
              )
            })}
          </div>
        </div>
      </div>
    </nav>
  )
}
