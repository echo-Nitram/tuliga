'use client'

import { useEffect, useState } from 'react'

interface Referee {
  id: number
  name: string
  level: string
}

export default function RefereesPage() {
  const [refs, setRefs] = useState<Referee[]>([])
  const [name, setName] = useState('')
  const [level, setLevel] = useState('regional')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const baseUrl = process.env.NEXT_PUBLIC_API_URL

  useEffect(() => {
    setLoading(true)
    fetch(`${baseUrl}/referees`)
      .then(res => {
        if (!res.ok) throw new Error(`Error ${res.status}`)
        return res.json()
      })
      .then(setRefs)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [baseUrl])

  async function addReferee(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${baseUrl}/referees`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, level })
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || `Error ${res.status}`)
      }
      const data = await res.json()
      setRefs([...refs, data])
      setName('')
    } catch (err: any) {
      setError(err.message)
    }
  }

  const levelLabel = (l: string) => {
    const map: Record<string, { text: string; color: string }> = {
      regional: { text: 'Regional', color: 'bg-blue-100 text-blue-700' },
      senior: { text: 'Senior', color: 'bg-amber-100 text-amber-700' },
    }
    return map[l] || { text: l, color: 'bg-gray-100 text-gray-600' }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-gray-400 text-lg">Cargando árbitros...</div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Árbitros</h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      <form onSubmit={addReferee} className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-8">
        <h2 className="text-lg font-semibold mb-3">Agregar árbitro</h2>
        <div className="flex flex-wrap gap-3 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm text-gray-500 mb-1">Nombre</label>
            <input
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="Ej: Andrés Cunha"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-1">Nivel</label>
            <select
              value={level}
              onChange={e => setLevel(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="regional">Regional</option>
              <option value="senior">Senior</option>
            </select>
          </div>
          <button
            type="submit"
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium px-6 py-2 rounded-lg transition-colors"
          >
            Agregar
          </button>
        </div>
      </form>

      {refs.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">
          No hay árbitros registrados
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="text-left px-5 py-3 text-sm font-semibold text-gray-600">Nombre</th>
                <th className="text-left px-5 py-3 text-sm font-semibold text-gray-600">Nivel</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {refs.map(r => {
                const lv = levelLabel(r.level)
                return (
                  <tr key={r.id} className="hover:bg-gray-50">
                    <td className="px-5 py-3 font-medium">{r.name}</td>
                    <td className="px-5 py-3">
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${lv.color}`}>
                        {lv.text}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
