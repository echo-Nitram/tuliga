'use client'

import { useEffect, useState } from 'react'

interface Tournament {
  id: number
  name: string
  format: string
  status: string
}

interface Fixture {
  id: number
  round: number
  home: string
  away: string
  home_goals: number | null
  away_goals: number | null
}

export default function TournamentsPage() {
  const [tournaments, setTournaments] = useState<Tournament[]>([])
  const [fixtures, setFixtures] = useState<Fixture[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [name, setName] = useState('')
  const [format, setFormat] = useState('round_robin')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const baseUrl = process.env.NEXT_PUBLIC_API_URL

  async function fetchTournaments() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${baseUrl}/tournaments`)
      if (!res.ok) throw new Error(`Error ${res.status}`)
      setTournaments(await res.json())
    } catch (err: any) {
      setError(err.message || 'Error loading tournaments')
    } finally {
      setLoading(false)
    }
  }

  async function fetchFixtures(tournamentId: number) {
    try {
      const res = await fetch(`${baseUrl}/tournaments/${tournamentId}/fixtures`)
      if (!res.ok) throw new Error(`Error ${res.status}`)
      setFixtures(await res.json())
    } catch (err: any) {
      setError(err.message)
    }
  }

  useEffect(() => {
    fetchTournaments()
  }, [])

  useEffect(() => {
    if (selectedId) fetchFixtures(selectedId)
    else setFixtures([])
  }, [selectedId])

  async function createTournament(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${baseUrl}/tournaments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, format })
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || `Error ${res.status}`)
      }
      const data = await res.json()
      setTournaments(prev => [...prev, data])
      setName('')
    } catch (err: any) {
      setError(err.message)
    }
  }

  async function generateFixtures(tournamentId: number) {
    setError(null)
    try {
      const res = await fetch(`${baseUrl}/tournaments/${tournamentId}/generate`, {
        method: 'POST'
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || `Error ${res.status}`)
      }
      const data = await res.json()
      setFixtures(data)
      fetchTournaments()
    } catch (err: any) {
      setError(err.message)
    }
  }

  const formatLabel = (f: string) =>
    f === 'round_robin' ? 'Todos contra todos' : 'Eliminación directa'

  const statusLabel = (s: string) => {
    const map: Record<string, { text: string; color: string }> = {
      draft: { text: 'Borrador', color: 'bg-gray-100 text-gray-600' },
      in_progress: { text: 'En curso', color: 'bg-emerald-100 text-emerald-700' },
      finished: { text: 'Finalizado', color: 'bg-blue-100 text-blue-700' },
    }
    return map[s] || { text: s, color: 'bg-gray-100 text-gray-600' }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-gray-400 text-lg">Cargando torneos...</div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Torneos</h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      <form onSubmit={createTournament} className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-8">
        <h2 className="text-lg font-semibold mb-3">Crear nuevo torneo</h2>
        <div className="flex flex-wrap gap-3 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm text-gray-500 mb-1">Nombre</label>
            <input
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="Ej: Apertura 2026"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-1">Formato</label>
            <select
              value={format}
              onChange={e => setFormat(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="round_robin">Todos contra todos</option>
              <option value="elimination">Eliminación directa</option>
            </select>
          </div>
          <button
            type="submit"
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium px-6 py-2 rounded-lg transition-colors"
          >
            Crear
          </button>
        </div>
      </form>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 className="text-lg font-semibold mb-3">Lista de Torneos</h2>
          {tournaments.length === 0 ? (
            <div className="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">
              No hay torneos creados todavía
            </div>
          ) : (
            <div className="space-y-3">
              {tournaments.map(t => {
                const status = statusLabel(t.status)
                const isSelected = selectedId === t.id
                return (
                  <div
                    key={t.id}
                    onClick={() => setSelectedId(t.id)}
                    className={`bg-white rounded-xl border p-4 cursor-pointer transition-all ${
                      isSelected
                        ? 'border-emerald-400 shadow-md ring-1 ring-emerald-200'
                        : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-gray-900">{t.name}</span>
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${status.color}`}>
                        {status.text}
                      </span>
                    </div>
                    <div className="text-sm text-gray-500">{formatLabel(t.format)}</div>
                    {t.status === 'draft' && (
                      <button
                        onClick={(e) => { e.stopPropagation(); generateFixtures(t.id) }}
                        className="mt-2 text-sm bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1 rounded-lg transition-colors"
                      >
                        Generar Fixture
                      </button>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-3">Fixture</h2>
          {!selectedId ? (
            <div className="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">
              Seleccioná un torneo para ver su fixture
            </div>
          ) : fixtures.length === 0 ? (
            <div className="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">
              Este torneo aún no tiene fixture generado
            </div>
          ) : (
            <div className="space-y-4">
              {Array.from(new Set(fixtures.map(f => f.round))).map(round => (
                <div key={round} className="bg-white rounded-xl border border-gray-200 p-4">
                  <h3 className="text-sm font-semibold text-emerald-700 mb-2">
                    Fecha {round}
                  </h3>
                  <div className="space-y-2">
                    {fixtures.filter(f => f.round === round).map(f => (
                      <div
                        key={f.id}
                        className="flex items-center justify-between text-sm bg-gray-50 rounded-lg px-3 py-2"
                      >
                        <span className="font-medium">{f.home}</span>
                        <span className="text-gray-400 mx-2">vs</span>
                        <span className="font-medium">{f.away}</span>
                        {f.home_goals !== null && f.away_goals !== null && (
                          <span className="ml-3 bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">
                            {f.home_goals} - {f.away_goals}
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
