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

  if (loading) return <div className="p-4">Cargando torneos...</div>

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Torneos</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={createTournament} className="mb-6 space-x-2">
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Nombre del torneo"
          className="border px-2 py-1"
          required
        />
        <select value={format} onChange={e => setFormat(e.target.value)} className="border px-2 py-1">
          <option value="round_robin">Todos contra todos</option>
          <option value="elimination">Eliminacion directa</option>
        </select>
        <button type="submit" className="bg-blue-500 text-white px-4 py-1 rounded">
          Crear Torneo
        </button>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-lg font-semibold mb-2">Lista de Torneos</h2>
          {tournaments.length === 0 ? (
            <p className="text-gray-500">No hay torneos creados</p>
          ) : (
            <ul className="space-y-2">
              {tournaments.map(t => (
                <li
                  key={t.id}
                  className={`p-3 border rounded cursor-pointer ${selectedId === t.id ? 'bg-blue-50 border-blue-400' : ''}`}
                  onClick={() => setSelectedId(t.id)}
                >
                  <div className="font-medium">{t.name}</div>
                  <div className="text-sm text-gray-500">
                    {t.format === 'round_robin' ? 'Todos contra todos' : 'Eliminacion'} | {t.status}
                  </div>
                  {t.status === 'draft' && (
                    <button
                      onClick={(e) => { e.stopPropagation(); generateFixtures(t.id) }}
                      className="mt-1 text-sm bg-green-500 text-white px-2 py-0.5 rounded"
                    >
                      Generar Fixture
                    </button>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2">Fixture</h2>
          {!selectedId ? (
            <p className="text-gray-500">Selecciona un torneo</p>
          ) : fixtures.length === 0 ? (
            <p className="text-gray-500">Sin fixture generado</p>
          ) : (
            <div className="space-y-3">
              {Array.from(new Set(fixtures.map(f => f.round))).map(round => (
                <div key={round}>
                  <h3 className="font-medium text-sm text-gray-600">Fecha {round}</h3>
                  <ul className="ml-2">
                    {fixtures.filter(f => f.round === round).map(f => (
                      <li key={f.id} className="text-sm">
                        {f.home} vs {f.away}
                        {f.home_goals !== null && f.away_goals !== null && (
                          <span className="ml-2 font-bold">({f.home_goals} - {f.away_goals})</span>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
